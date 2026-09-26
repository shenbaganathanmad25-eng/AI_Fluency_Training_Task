"""Creates big_stock.html: a large page used to trigger the context-overflow failure."""
rows = "\n".join(
    f"<tr><td>Batch GP{n:04d}</td><td>Medicine PARA01</td>"
    f"<td>Expiry 2027-{1 + n % 12:02d}</td><td>Remarks: stored at room temperature</td></tr>"
    for n in range(1, 3001))
html = f"<html><body><h1>Batch Ledger</h1><table>{rows}</table></body></html>"
open("big_stock.html", "w", encoding="utf-8").write(html)
print(f"big_stock.html created: {len(html):,} characters")