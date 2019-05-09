# 已经购买的金额和数量
havePrice = 6.29
haveNum = 3000

# 想要补仓的金额和数量
willPrice = 6.12
willNum = 500

# 获取分摊后的成本价
price = (haveNum * havePrice + willNum * willPrice)/(haveNum + willNum)

print(price)

