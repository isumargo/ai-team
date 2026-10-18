import re

def parse_message(text: str) -> dict:
    text = text.strip()
    
    # JUAL [produk] [qty] bks [reseller] [harga opsional]
    # Example: "JUAL madju pro 100 bks ke rudi 8500" or "Jual Sukses Alami 50 bks Ichsan"
    # Regex: (JUAL) (product) (qty) bks (reseller) (price?)
    # Since product and reseller names can have spaces, this is tricky.
    # Let's try to match keywords.
    
    jual_match = re.match(r'^(JUAL|jual)\s+(.+?)\s+(\d+)\s+bks\s+(.+?)(?:\s+(\d+))?$', text, re.IGNORECASE)
    if jual_match:
        return {
            'action': 'JUAL',
            'product': jual_match.group(2).strip(),
            'qty': int(jual_match.group(3)),
            'reseller': jual_match.group(4).strip(),
            'price': int(jual_match.group(5)) if jual_match.group(5) else None
        }

    # CONTOH [produk] [qty] bks [reseller]
    contoh_match = re.match(r'^(CONTOH|contoh)\s+(.+?)\s+(\d+)\s+bks\s+(.+)$', text, re.IGNORECASE)
    if contoh_match:
        return {
            'action': 'CONTOH',
            'product': contoh_match.group(2).strip(),
            'qty': int(contoh_match.group(3)),
            'reseller': contoh_match.group(4).strip()
        }

    # RETUR [produk] [qty] bks [reseller]
    retur_match = re.match(r'^(RETUR|retur)\s+(.+?)\s+(\d+)\s+bks\s+(.+)$', text, re.IGNORECASE)
    if retur_match:
        return {
            'action': 'RETUR',
            'product': retur_match.group(2).strip(),
            'qty': int(retur_match.group(3)),
            'reseller': retur_match.group(4).strip()
        }

    # STOK [produk]
    stok_prod_match = re.match(r'^(STOK|stok)\s+(.+)$', text, re.IGNORECASE)
    if stok_prod_match:
        return {
            'action': 'STOK',
            'product': stok_prod_match.group(2).strip()
        }

    # STOK
    if text.upper() == 'STOK':
        return {
            'action': 'STOK',
            'product': None
        }

    # PIUTANG [reseller]
    piutang_match = re.match(r'^(PIUTANG|piutang)\s+(.+)$', text, re.IGNORECASE)
    if piutang_match:
        return {
            'action': 'PIUTANG',
            'reseller': piutang_match.group(2).strip()
        }
    
    # PIUTANG (all)
    if text.upper() == 'PIUTANG':
        return {
            'action': 'PIUTANG',
            'reseller': None
        }

    return {'error': 'Format tidak dikenali.'}
