#!/usr/bin/env python3
"""PACP annual membership policy model — offline tests, NOT server authorization.
Policy proposal only; does not write to Supabase or issue cards.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import unittest

PALESTINE = ZoneInfo("Asia/Hebron")

@dataclass(frozen=True)
class MemberPeriod:
    year: int
    status: str
    settled: bool
    activated_at: datetime | None
    revoked: bool = False
    suspended: bool = False
    code: str | None = None

def expires_at(year: int) -> datetime:
    """Exclusive UTC expiry: 00:00 local Jan 1 of following year."""
    return datetime(year + 1, 1, 1, tzinfo=PALESTINE).astimezone(timezone.utc)

def card_eligible(period: MemberPeriod | None, now: datetime) -> bool:
    if period is None or now.tzinfo is None:
        return False
    if period.status != "active" or not period.settled:
        return False
    if period.revoked or period.suspended or not period.code:
        return False
    if period.activated_at is None or period.activated_at.tzinfo is None:
        return False
    instant = now.astimezone(timezone.utc)
    return period.activated_at.astimezone(timezone.utc) <= instant < expires_at(period.year)

class AnnualPolicyTest(unittest.TestCase):
    def setUp(self):
        self.period = MemberPeriod(2027, "active", True,
            datetime(2027, 1, 1, tzinfo=PALESTINE), code="PACP-2027-0001")

    def test_last_day_of_year_is_valid(self):
        self.assertTrue(card_eligible(self.period, datetime(2027,12,31,23,59,59,tzinfo=PALESTINE)))

    def test_midnight_january_first_expires(self):
        self.assertFalse(card_eligible(self.period, datetime(2028,1,1,0,0,tzinfo=PALESTINE)))

    def test_january_administrative_grace_does_not_extend_qr(self):
        self.assertFalse(card_eligible(self.period, datetime(2028,1,15,tzinfo=PALESTINE)))

    def test_approved_alone_is_insufficient(self):
        self.assertFalse(card_eligible(MemberPeriod(2027,"approved",True,
            self.period.activated_at,code=self.period.code), datetime(2027,6,1,tzinfo=PALESTINE)))

    def test_unsettled_and_no_code_are_ineligible(self):
        at = datetime(2027,6,1,tzinfo=PALESTINE)
        self.assertFalse(card_eligible(MemberPeriod(2027,"active",False,self.period.activated_at,code=self.period.code),at))
        self.assertFalse(card_eligible(MemberPeriod(2027,"active",True,self.period.activated_at),at))

    def test_suspension_revocation_and_other_states_are_ineligible(self):
        at = datetime(2027,6,1,tzinfo=PALESTINE)
        for state in ("suspended","expired","revoked","approved_pending_activation"):
            self.assertFalse(card_eligible(MemberPeriod(2027,state,True,self.period.activated_at,code=self.period.code),at))
        self.assertFalse(card_eligible(MemberPeriod(2027,"active",True,self.period.activated_at,suspended=True,code=self.period.code),at))
        self.assertFalse(card_eligible(MemberPeriod(2027,"active",True,self.period.activated_at,revoked=True,code=self.period.code),at))

    def test_not_active_before_activation(self):
        self.assertFalse(card_eligible(self.period,datetime(2026,12,31,tzinfo=PALESTINE)))

    def test_renewal_period_separate_and_number_preserved(self):
        p28 = MemberPeriod(2028,"active",True,datetime(2028,1,1,tzinfo=PALESTINE),code=self.period.code)
        self.assertTrue(card_eligible(p28,datetime(2028,1,1,tzinfo=PALESTINE)))
        self.assertFalse(card_eligible(self.period,datetime(2028,1,1,tzinfo=PALESTINE)))

if __name__ == "__main__":
    unittest.main()
