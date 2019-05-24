'''
Given the string returned from the OCR algorithm, scrape for the bank number
'''
def find_credit_num(s):
    digits = [str(a) for a in range(0, 10)]

    '''
    Check if the number block comprises of only digits
    '''
    def is_number(chunk):
        for c in chunk:
            if c not in digits:
                return False
        return True

    chunks = s.split(' ')
    ret = []
    tmp = []
    for chunk in chunks:
        if is_number(chunk) and len(tmp) < 4:
            tmp.append(chunk)
        else:
            ret.append(tmp.copy())
            tmp = []
    ret.sort(key = lambda x: abs(4-len(x)))
    return ' '.join(ret[0])

strs = [
    "GIFT CARD 4358 8054 7198 2225 4358 DEBIT 1224 VISA GIFT CARD RECIPIENT VALID ONLY IN THE UNITED STATES",
    "US and Canada 800.421 2110 international Collect 30273857าร A AUTHORIZED SIGNATURE cull MICHAEL WAN 5524 3348 8020 7625 Valid Thru: 01/24 Cardholder Since 18"
]

parsed = strs[0]
print(find_credit_num(parsed))