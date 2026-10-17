# Ltd + Wise + billing plan
**Trigger (owner decision 17 Oct): jaise hi 3–4 free trial signups aayein, foran shuru karein**, taake trial khatam hone (7 din) tak subscription lene ka system tayyar ho.

## Order (trial signups 3–4 hote hi)
1. [ ] Companies House: naam check → Ltd register (online, aam taur par ~24 ghante; fee gov.uk par check)
2. [ ] Wise Business account, Ltd ke naam par (verification mein kuch din lag sakte hain, is liye pehle din apply)
3. [ ] Monthly billing: Stripe (card, subscriptions + payment links) ya GoCardless (direct debit). Payout = Wise account (sort code + account number)
4. [ ] Har Fellow ka subscription link banana (£59/£129/£69/£89/£119/£149/£389) → main trial-end email aur service pages par "Start subscription" button laga doonga
5. [ ] Trial khatam hone se 1 din pehle har trial client ko email: kya mila + subscription link

## Pehli payment ke baad
## Company (Ltd)
- [ ] Companies House par Ltd register karein (online; fee check karein gov.uk par). Naam: "ContentFellow Ltd" available hai? Pehle Companies House name search.
- [ ] Business bank account (company ke naam par), aur payments wahan shift.
- [ ] HMRC: Corporation Tax registration (company banne ke baad automatically letter aata hai, 3 mahine ke andar register).
- [ ] ICO data protection fee (form se leads collect ho rahi hain): ico.org.uk par fee check aur pay.
- [ ] VAT: £90,000 sales (12 mahine) se pehle zaroori nahi. Voluntary registration ka faisla accountant se. Jab tak registered nahi, site par "no VAT added" sahi hai.

## Website par update (main kar doonga, 15 min)
- [ ] Footer + /about/: "ContentFellow Ltd, registered in England & Wales, company no. ______, registered office ______" (UK law: Ltd websites par yeh dikhana zaroori hai)
- [ ] /about/ + homepage schema: legalName, Companies House URL in sameAs (GEO entity signal; AI "is ContentFellow legit" prompt)
- [ ] Privacy notice: controller = ContentFellow Ltd
- [ ] Agar VAT register ho: FAQ "Are prices plus VAT?" + about facts + comparison posts update (tools/build_pages.py)
- [ ] Directories (citation-pack.md): sab par legal naam/number update; Companies House naam = site naam
