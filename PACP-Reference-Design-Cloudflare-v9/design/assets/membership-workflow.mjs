const transitions = {
  draft: { applicant: ['submitted'] },
  submitted: { reviewer: ['needs_changes', 'approved', 'rejected'] },
  needs_changes: { applicant: ['submitted'] },
};

export function advance(application, actor, status, reason = '') {
  if (!transitions[application.status]?.[actor]?.includes(status)) {
    throw new Error('هذا الإجراء غير متاح في الحالة الحالية.');
  }
  reason = reason.trim();
  if (['needs_changes', 'rejected'].includes(status) && !reason) {
    throw new Error('يرجى إدخال سبب القرار التجريبي.');
  }
  return {
    ...application,
    status,
    membershipCode: status === 'approved' ? `DEMO-PACP-${String(application.id).padStart(3, '0')}` : null,
    history: [...application.history, { actor, status, reason }],
  };
}
