-- PACP application payload shape validator — REVIEW DRAFT ONLY
-- No new public RPC; no eligibility approval or documents policy implied.
-- Can be used by a future trusted submission endpoint after independent review.
begin;
create or replace function public.membership_payload_shape_errors(p_data jsonb)
returns jsonb
language plpgsql immutable
set search_path = pg_catalog, public
as $$
declare
  k text;
  required_keys text[] := array[
    'name_ar_first','name_ar_father','name_ar_grandfather','name_ar_family',
    'name_en_first','name_en_father','name_en_grandfather','name_en_family',
    'email'
  ];
  errs jsonb := '[]'::jsonb;
begin
  if p_data is null or jsonb_typeof(p_data) <> 'object' then
    return jsonb_build_array('payload_must_be_object');
  end if;
  if pg_column_size(p_data) > 16384 then
    errs := errs || jsonb_build_array('payload_too_large');
  end if;
  foreach k in array required_keys loop
    if jsonb_typeof(p_data->k) is distinct from 'string'
       or length(btrim(coalesce(p_data->>k,''))) = 0
       or length(p_data->>k) > 150 then
      errs := errs || jsonb_build_array('invalid_' || k);
    end if;
  end loop;
  if jsonb_typeof(p_data->'email') = 'string'
     and (length(p_data->>'email') > 254
          or (p_data->>'email') !~* '^[^[:space:]@]+@[^[:space:]@]+[.][^[:space:]@]+$') then
    errs := errs || jsonb_build_array('invalid_email_format');
  end if;
  if p_data ? 'graduation_year' and p_data->>'graduation_year' is not null
     and (jsonb_typeof(p_data->'graduation_year') <> 'number'
          or (p_data->>'graduation_year') !~ '^[0-9]{4}$'
          or (p_data->>'graduation_year')::int not between 1950 and 2100) then
    errs := errs || jsonb_build_array('invalid_graduation_year');
  end if;
  if p_data ? 'has_moh_practice_license'
     and jsonb_typeof(p_data->'has_moh_practice_license') <> 'boolean' then
    errs := errs || jsonb_build_array('invalid_moh_license_flag');
  end if;
  return errs;
end;
$$;
revoke all on function public.membership_payload_shape_errors(jsonb) from public, anon, authenticated;
commit;
-- This checks syntax only. It does not prove identity, qualifications, consent,
-- document authenticity, legal eligibility, payment or authorization.
-- IMPORTANT: reconcile submitted_data key names with the final membership form.
-- No browser-exposed grants, triggers, or production usage until reviewed.
