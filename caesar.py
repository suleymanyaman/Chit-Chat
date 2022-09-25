
alphabet = "ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZabcçdefgğhıijklmnoöpqrsştuüvwxyz0123456789"


def cipher(text, inc): 

    target = ""
    
    for i in text:
        if i.isalnum():
            index = alphabet.index(i) + inc 
            try: 
                target = target + alphabet[index]
            except IndexError: 
                target = target + alphabet[len(alphabet)-inc]
        else:
            target = target + i


    return target 


def decipher(text, inc):

    target = ""
    for i in text:
        if i.isalnum():
            index = alphabet.index(i) - inc
            target = target + alphabet[index]
        else:
            target = target + i

    return target 
