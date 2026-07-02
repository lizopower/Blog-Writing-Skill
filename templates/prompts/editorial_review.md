# Editorial review prompt

Eight-dimension taste review. Write editorial_review.md with Publishability: PASS or FAIL.

Dimensions: topic selection, angle / differentiation, structure, evidence use, tone,
cross-article voice diversity, CTA, publishability.

The "cross-article voice diversity" dimension applies only when this article is one of a
cluster/series written together. Read the sibling drafts and run
`skills/tech-blog-writer/scripts/cluster_voice_check.py --root <root> --slugs <a,b,c> --write-report`;
fold its findings in. Any cross-article issue (shared opener, shared AI cliche, repeated
phrasing, matching cadence) drives this dimension to 1-2 and fails Publishability. Score it
`N/A` for standalone articles. See standards/cluster_voice_guide.md.
