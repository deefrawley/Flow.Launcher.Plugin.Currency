# -*- coding: utf-8 -*-


from plugin import Main

if __name__ == "__main__":
    r = Main().query("cc 46000 GBP AUD")
    print(r)