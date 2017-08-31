import logging
import os

from foolspider import settings
from foolspider.items import SecurityItem
from foolspider.utils.utils import get_balance_sheet_path, detect_encoding, get_income_statement_path, \
    get_cash_flow_statement_path

logger = logging.getLogger(__name__)


def get_balance_sheet_items(security_item):
    path = get_balance_sheet_path(security_item)
    if not os.path.exists(path):
        return None
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')

    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()

        # for idx, line in enumerate(lines):
        #     yield idx, line.split()

        reportDate = lines[0].split()[1:-1]
        # 货币资金
        moneyFunds = lines[3].split()[1:-1]
        # 交易性金融资产
        heldForTradingFinancialAssets = lines[4].split()[1:-1]
        # 衍生金融资产
        derivative = lines[5].split()[1:-1]
        # 应收票据
        billsReceivable = lines[6].split()[1:-1]
        # 应收账款
        accountsReceivable = lines[7].split()[1:-1]
        # 预付款项
        prepaidAccounts = lines[8].split()[1:-1]
        # 应收利息
        interestReceivable = lines[9].split()[1:-1]
        # 应收股利
        dividendReceivable = lines[10].split()[1:-1]
        # 其他应收款
        otherReceivables = lines[11].split()[1:-1]

        # 买入返售金融资产
        buyingBackTheSaleOfFinancialAssets = lines[12].split()[1:-1]
        # 存货
        inventory = lines[13].split()[1:-1]
        # 划分为持有待售的资产
        assetsForSale = lines[14].split()[1:-1]
        # 一年内到期的非流动资产
        nonCurrentAssetsDueWithinOneYear = lines[15].split()[1:-1]

        # 待摊费用
        unamortizedExpenditures = lines[16].split()[1:-1]
        # 待处理流动资产损益
        waitDealIntangibleAssetsLossOrIncome = lines[17].split()[1:-1]

        # 其他流动资产
        otherCurrentAssets = lines[18].split()[1:-1]
        # 流动资产合计
        totalCurrentAssets = lines[19].split()[1:-1]

        # 非流动资产

        # 发放贷款及垫款
        loansAndPaymentsOnBehalf = lines[21].split()[1:-1]

        # 可供出售金融资产
        availableForSaleFinancialAssets = lines[22].split()[1:-1]
        # 持有至到期投资
        heldToMaturityInvestment = lines[23].split()[1:-1]
        # 长期应收款
        longTermReceivables = lines[24].split()[1:-1]
        # 长期股权投资
        longTermEquityInvestment = lines[25].split()[1:-1]
        # 投资性房地产
        investmentRealEstate = lines[26].split()[1:-1]
        # 固定资产净额
        NetfixedAssets = lines[27].split()[1:-1]
        # 在建工程
        constructionInProcess = lines[28].split()[1:-1]
        # 工程物资
        engineerMaterial = lines[29].split()[1:-1]
        # 固定资产清理
        fixedAssetsInLiquidation = lines[30].split()[1:-1]
        # 生产性生物资产
        productiveBiologicalAssets = lines[31].split()[1:-1]
        # 公益性生物资产
        nonProfitLivingAssets = lines[32].split()[1:-1]
        # 油气资产
        oilAndGasAssets = lines[33].split()[1:-1]
        # 无形资产
        intangibleAssets = lines[34].split()[1:-1]
        # 开发支出
        developmentExpenditure = lines[35].split()[1:-1]
        # 商誉
        goodwill = lines[36].split()[1:-1]
        # 长期待摊费用
        longTermDeferredExpenses = lines[37].split()[1:-1]
        # 递延所得税资产
        deferredIncomeTaxAssets = lines[38].split()[1:-1]
        # 其他非流动资产
        OtherNonCurrentAssets = lines[39].split()[1:-1]
        # 非流动资产合计
        nonCurrentAssets = lines[40].split()[1:-1]
        # 资产总计
        totalAssets = lines[41].split()[1:-1]

        # / *流动负债 * /
        # 短期借款
        shortTermBorrowing = lines[43].split()[1:-1]
        # 交易性金融负债
        transactionFinancialLiabilities = lines[44].split()[1:-1]
        # 应付票据
        billsPayable = lines[45].split()[1:-1]
        # 应付账款
        accountsPayable = lines[46].split()[1:-1]
        # 预收款项
        accountsReceivedInAdvance = lines[47].split()[1:-1]
        # 应付手续费及佣金
        handlingChargesAndCommissionsPayable = lines[48].split()[1:-1]
        # 应付职工薪酬
        employeeBenefitsPayable = lines[49].split()[1:-1]
        # 应交税费
        taxesAndSurchargesPayable = lines[50].split()[1:-1]
        # 应付利息
        interestPayable = lines[51].split()[1:-1]
        # 应付股利
        dividendpayable = lines[52].split()[1:-1]
        # 其他应付款
        otherPayables = lines[53].split()[1:-1]
        # 预提费用
        withholdingExpenses = lines[54].split()[1:-1]
        # 一年内的递延收益
        deferredIncomeWithinOneYear = lines[55].split()[1:-1]
        # 应付短期债券
        shortTermDebenturesPayable = lines[56].split()[1:-1]
        # 一年内到期的非流动负债
        nonCurrentLiabilitiesMaturingWithinOneYear = lines[57].split()[1:-1]
        # 其他流动负债
        otherCurrentLiability = lines[58].split()[1:-1]
        # 流动负债合计
        totalCurrentLiabilities = lines[59].split()[1:-1]

        # / *非流动负债 * /
        # 长期借款
        LongTermBorrowing = lines[61].split()[1:-1]
        # 应付债券
        bondPayable = lines[62].split()[1:-1]
        # 长期应付款
        longTermPayables = lines[63].split()[1:-1]
        # 长期应付职工薪酬
        longTermEmployeeBenefitsPayable = lines[64].split()[1:-1]
        # 专项应付款
        specialPayable = lines[65].split()[1:-1]
        # 预计非流动负债
        expectedNonCurrentLiabilities = lines[66].split()[1:-1]
        # 递延所得税负债
        deferredIncomeTaxLiabilities = lines[67].split()[1:-1]
        # 长期递延收益
        longTermDeferredRevenue = lines[68].split()[1:-1]
        # 其他非流动负债
        otherNonCurrentLiabilities = lines[69].split()[1:-1]
        # 非流动负债合计
        totalNonCurrentLiabilities = lines[70].split()[1:-1]
        # 负债合计
        totalLiabilities = lines[71].split()[1:-1]

        # / *所有者权益 * /
        # 实收资本(或股本)
        registeredCapital = lines[73].split()[1:-1]

        # 资本公积
        capitalSurplus = lines[74].split()[1:-1]
        # 减：库存股
        treasuryStock = lines[75].split()[1:-1]
        # 其他综合收益
        otherComprehensiveIncome = lines[76].split()[1:-1]
        # 专项储备
        theSpecialReserve = lines[77].split()[1:-1]

        # 盈余公积
        surplusReserves = lines[78].split()[1:-1]
        # 一般风险准备
        generalRiskPreparation = lines[79].split()[1:-1]
        # 未分配利润
        undistributedProfits = lines[80].split()[1:-1]
        # 归属于母公司股东权益合计
        consolidatedIncomeBelongingToParentCompany = lines[81].split()[1:-1]

        # 少数股东权益
        minorityStockholderInterest = lines[82].split()[1:-1]

        # 所有者权益(或股东权益)合计
        totalInvestorsEquity = lines[83].split()[1:-1]

        # 负债和所有者权益(或股东权益)总计
        totalLiabilitiesAndOwnersEquity = lines[84].split()[1:-1]

        for idx, _ in enumerate(reportDate):
            yield {
                "reportDate": reportDate[idx],
                "securityId": security_item["id"],
                "code": security_item["code"],
                # 货币资金
                "moneyFunds": moneyFunds[idx],
                # 交易性金融资产
                "heldForTradingFinancialAssets": heldForTradingFinancialAssets[idx],
                # 衍生金融资产
                "derivative": derivative[idx],
                # 应收票据
                "billsReceivable": billsReceivable[idx],
                # 应收账款
                "accountsReceivable": accountsReceivable[idx],
                # 预付款项
                "prepaidAccounts": prepaidAccounts[idx],
                # 应收利息
                "interestReceivable": interestReceivable[idx],
                # 应收股利
                "dividendReceivable": dividendReceivable[idx],
                # 其他应收款
                "otherReceivables": otherReceivables[idx],

                # 买入返售金融资产
                "buyingBackTheSaleOfFinancialAssets": buyingBackTheSaleOfFinancialAssets[idx],
                # 存货
                "inventory": inventory[idx],
                # 划分为持有待售的资产
                "assetsForSale": assetsForSale[idx],
                # 一年内到期的非流动资产
                "nonCurrentAssetsDueWithinOneYear": nonCurrentAssetsDueWithinOneYear[idx],

                # 待摊费用
                "unamortizedExpenditures": unamortizedExpenditures[idx],
                # 待处理流动资产损益
                "waitDealIntangibleAssetsLossOrIncome": waitDealIntangibleAssetsLossOrIncome[idx],

                # 其他流动资产
                "otherCurrentAssets": otherCurrentAssets[idx],
                # 流动资产合计
                "totalCurrentAssets": totalCurrentAssets[idx],

                # 非流动资产

                # 发放贷款及垫款
                "loansAndPaymentsOnBehalf": loansAndPaymentsOnBehalf[idx],

                # 可供出售金融资产
                "availableForSaleFinancialAssets": availableForSaleFinancialAssets[idx],
                # 持有至到期投资
                "heldToMaturityInvestment": heldToMaturityInvestment[idx],
                # 长期应收款
                "longTermReceivables": longTermReceivables[idx],
                # 长期股权投资
                "longTermEquityInvestment": longTermEquityInvestment[idx],
                # 投资性房地产
                "investmentRealEstate": investmentRealEstate[idx],
                # 固定资产净额
                "NetfixedAssets": NetfixedAssets[idx],
                # 在建工程
                "constructionInProcess": constructionInProcess[idx],
                # 工程物资
                "engineerMaterial": engineerMaterial[idx],
                # 固定资产清理
                "fixedAssetsInLiquidation": fixedAssetsInLiquidation[idx],
                # 生产性生物资产
                "productiveBiologicalAssets": productiveBiologicalAssets[idx],
                # 公益性生物资产
                "nonProfitLivingAssets": nonProfitLivingAssets[idx],
                # 油气资产
                "oilAndGasAssets": oilAndGasAssets[idx],
                # 无形资产
                "intangibleAssets": intangibleAssets[idx],
                # 开发支出
                "developmentExpenditure": developmentExpenditure[idx],
                # 商誉
                "goodwill": goodwill[idx],
                # 长期待摊费用
                "longTermDeferredExpenses": longTermDeferredExpenses[idx],
                # 递延所得税资产
                "deferredIncomeTaxAssets": deferredIncomeTaxAssets[idx],
                # 其他非流动资产
                "OtherNonCurrentAssets": OtherNonCurrentAssets[idx],
                # 非流动资产合计
                "nonCurrentAssets": nonCurrentAssets[idx],
                # 资产总计
                "totalAssets": totalAssets[idx],

                # / *流动负债 * /
                # 短期借款
                "shortTermBorrowing": shortTermBorrowing[idx],
                # 交易性金融负债
                "transactionFinancialLiabilities": transactionFinancialLiabilities[idx],
                # 应付票据
                "billsPayable": billsPayable[idx],
                # 应付账款
                "accountsPayable": accountsPayable[idx],
                # 预收款项
                "accountsReceivedInAdvance": accountsReceivedInAdvance[idx],
                # 应付手续费及佣金
                "handlingChargesAndCommissionsPayable": handlingChargesAndCommissionsPayable[idx],
                # 应付职工薪酬
                "employeeBenefitsPayable": employeeBenefitsPayable[idx],
                # 应交税费
                "taxesAndSurchargesPayable": taxesAndSurchargesPayable[idx],
                # 应付利息
                "interestPayable": interestPayable[idx],
                # 应付股利
                "dividendpayable": dividendpayable[idx],
                # 其他应付款
                "otherPayables": otherPayables[idx],
                # 预提费用
                "withholdingExpenses": withholdingExpenses[idx],
                # 一年内的递延收益
                "deferredIncomeWithinOneYear": deferredIncomeWithinOneYear[idx],
                # 应付短期债券
                "shortTermDebenturesPayable": shortTermDebenturesPayable[idx],
                # 一年内到期的非流动负债
                "nonCurrentLiabilitiesMaturingWithinOneYear": nonCurrentLiabilitiesMaturingWithinOneYear[idx],
                # 其他流动负债
                "otherCurrentLiability": otherCurrentLiability[idx],
                # 流动负债合计
                "totalCurrentLiabilities": totalCurrentLiabilities[idx],

                # / *非流动负债 * /
                # 长期借款
                "LongTermBorrowing": LongTermBorrowing[idx],
                # 应付债券
                "bondPayable": bondPayable[idx],
                # 长期应付款
                "longTermPayables": longTermPayables[idx],
                # 长期应付职工薪酬
                "longTermEmployeeBenefitsPayable": longTermEmployeeBenefitsPayable[idx],
                # 专项应付款
                "specialPayable": specialPayable[idx],
                # 预计非流动负债
                "expectedNonCurrentLiabilities": expectedNonCurrentLiabilities[idx],
                # 递延所得税负债
                "deferredIncomeTaxLiabilities": deferredIncomeTaxLiabilities[idx],
                # 长期递延收益
                "longTermDeferredRevenue": longTermDeferredRevenue[idx],
                # 其他非流动负债
                "otherNonCurrentLiabilities": otherNonCurrentLiabilities[idx],
                # 非流动负债合计
                "totalNonCurrentLiabilities": totalNonCurrentLiabilities[idx],
                # 负债合计
                "totalLiabilities": totalLiabilities[idx],

                # / *所有者权益 * /
                # 实收资本(或股本)
                "registeredCapital": registeredCapital[idx],

                # 资本公积
                "capitalSurplus": capitalSurplus[idx],
                # 减：库存股
                "treasuryStock": treasuryStock[idx],
                # 其他综合收益
                "otherComprehensiveIncome": otherComprehensiveIncome[idx],
                # 专项储备
                "theSpecialReserve": theSpecialReserve[idx],

                # 盈余公积
                "surplusReserves": surplusReserves[idx],
                # 一般风险准备
                "generalRiskPreparation": generalRiskPreparation[idx],
                # 未分配利润
                "undistributedProfits": undistributedProfits[idx],
                # 归属于母公司股东权益合计
                "consolidatedIncomeBelongingToParentCompany": consolidatedIncomeBelongingToParentCompany[idx],

                # 少数股东权益
                "minorityStockholderInterest": minorityStockholderInterest[idx],

                # 所有者权益(或股东权益)合计
                "totalInvestorsEquity": totalInvestorsEquity[idx],

                # 负债和所有者权益(或股东权益)总计
                "totalLiabilitiesAndOwnersEquity": totalLiabilitiesAndOwnersEquity[idx]
            }


def get_income_statement_items(security_item):
    path = get_income_statement_path(security_item)
    if not os.path.exists(path):
        return None
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')

    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()
        # for idx, line in enumerate(lines):
        #     yield idx, line.split()

        reportDate = lines[0].split()[1:-1]
        # /*营业总收入*/
        # 营业收入
        operatingRevenue = lines[2].split()[1:-1]
        # /*营业总成本*/
        OperatingTotalCosts = lines[4].split()[1:-1]
        # 营业成本
        OperatingCosts = lines[5].split()[1:-1]
        # 营业税金及附加
        businessTaxesAndSurcharges = lines[6].split()[1:-1]
        # 销售费用
        sellingExpenses = lines[7].split()[1:-1]
        # 管理费用
        ManagingCosts = lines[8].split()[1:-1]
        # 财务费用
        financingExpenses = lines[9].split()[1:-1]
        # 资产减值损失
        assetsDevaluation = lines[10].split()[1:-1]
        # 公允价值变动收益
        incomeFromChangesInFairValue = lines[11].split()[1:-1]
        # 投资收益
        investmentIncome = lines[12].split()[1:-1]
        # 其中:对联营企业和合营企业的投资收益
        investmentIncomeFromRelatedEnterpriseAndJointlyOperating = lines[13].split()[1:-1]
        # 汇兑收益
        exchangeGains = lines[14].split()[1:-1]
        # /*营业利润*/
        salesProfit = lines[15].split()[1:-1]
        # 加:营业外收入
        nonOperatingIncome = lines[16].split()[1:-1]
        # 减：营业外支出
        nonOperatingExpenditure = lines[17].split()[1:-1]
        # 其中：非流动资产处置损失
        disposalLossOnNonCurrentLiability = lines[18].split()[1:-1]
        # /*利润总额*/
        totalProfits = lines[19].split()[1:-1]
        # 减：所得税费用
        incomeTaxExpense = lines[20].split()[1:-1]
        # /*净利润*/
        netProfit = lines[21].split()[1:-1]
        # 归属于母公司所有者的净利润
        netProfitAttributedToParentCompanyOwner = lines[22].split()[1:-1]
        # 少数股东损益
        minorityInterestIncome = lines[23].split()[1:-1]
        # /*每股收益*/
        # 基本每股收益(元/股)
        basicEarningsPerShare = lines[25].split()[1:-1]
        # 稀释每股收益(元/股)
        fullyDilutedEarningsPerShare = lines[26].split()[1:-1]
        # /*其他综合收益*/
        otherComprehensiveIncome = lines[27].split()[1:-1]
        # /*综合收益总额*/
        accumulatedOtherComprehensiveIncome = lines[28].split()[1:-1]
        # 归属于母公司所有者的综合收益总额
        attributableToOwnersOfParentCompany = lines[29].split()[1:-1]
        # 归属于少数股东的综合收益总额
        attributableToMinorityShareholders = lines[30].split()[1:-1]
    for idx, _ in enumerate(reportDate):
        yield {
            "reportDate": reportDate[idx],
            "securityId": security_item["id"],
            "code": security_item["code"],
            # /*营业总收入*/
            # 营业收入
            "operatingRevenue": operatingRevenue[idx],
            # /*营业总成本*/
            "OperatingTotalCosts": OperatingTotalCosts[idx],
            # 营业成本
            "OperatingCosts": OperatingCosts[idx],
            # 营业税金及附加
            "businessTaxesAndSurcharges": businessTaxesAndSurcharges[idx],
            # 销售费用
            "sellingExpenses": sellingExpenses[idx],
            # 管理费用
            "ManagingCosts": ManagingCosts[idx],
            # 财务费用
            "financingExpenses": financingExpenses[idx],
            # 资产减值损失
            "assetsDevaluation": assetsDevaluation[idx],
            # 公允价值变动收益
            "incomeFromChangesInFairValue": incomeFromChangesInFairValue[idx],
            # 投资收益
            "investmentIncome": investmentIncome[idx],
            # 其中:对联营企业和合营企业的投资收益
            "investmentIncomeFromRelatedEnterpriseAndJointlyOperating":
                investmentIncomeFromRelatedEnterpriseAndJointlyOperating[idx],
            # 汇兑收益
            "exchangeGains": exchangeGains[idx],
            # /*营业利润*/
            "salesProfit": salesProfit[idx],
            # 加:营业外收入
            "nonOperatingIncome": nonOperatingIncome[idx],
            # 减：营业外支出
            "nonOperatingExpenditure": nonOperatingExpenditure[idx],
            # 其中：非流动资产处置损失
            "disposalLossOnNonCurrentLiability": disposalLossOnNonCurrentLiability[idx],
            # /*利润总额*/
            "totalProfits": totalProfits[idx],
            # 减：所得税费用
            "incomeTaxExpense": incomeTaxExpense[idx],
            # /*净利润*/
            "netProfit": netProfit[idx],
            # 归属于母公司所有者的净利润
            "netProfitAttributedToParentCompanyOwner": netProfitAttributedToParentCompanyOwner[idx],
            # 少数股东损益
            "minorityInterestIncome": minorityInterestIncome[idx],
            # /*每股收益*/
            # 基本每股收益(元/股)
            "basicEarningsPerShare": basicEarningsPerShare[idx],
            # 稀释每股收益(元/股)
            "fullyDilutedEarningsPerShare": fullyDilutedEarningsPerShare[idx],
            # /*其他综合收益*/
            "otherComprehensiveIncome": otherComprehensiveIncome[idx],
            # /*综合收益总额*/
            "accumulatedOtherComprehensiveIncome": accumulatedOtherComprehensiveIncome[idx],
            # 归属于母公司所有者的综合收益总额
            "attributableToOwnersOfParentCompany": attributableToOwnersOfParentCompany[idx],
            # 归属于少数股东的综合收益总额
            "attributableToMinorityShareholders": attributableToMinorityShareholders[idx]
        }


def get_cash_flow_statement_items(security_item):
    path = get_cash_flow_statement_path(security_item)
    if not os.path.exists(path):
        return None
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')

    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()
        # for idx, line in enumerate(lines):
        #     yield idx, line.split()
        reportDate = lines[0].split()[1:-1]
        # /*一、经营活动产生的现金流量*/
        # 销售商品、提供劳务收到的现金
        cashFromSellingCommoditiesOrOfferingLabor = lines[3].split()[1:-1]
        # 收到的税费返还
        refundOfTaxAndFeeReceived = lines[4].split()[1:-1]
        # 收到的其他与经营活动有关的现金
        cashReceivedRelatingToOtherOperatingActivities = lines[5].split()[1:-1]
        # 经营活动现金流入小计
        subTotalOfCashInflowsFromOperatingActivities = lines[6].split()[1:-1]
        # 购买商品、接受劳务支付的现金
        cashPaidForGoodsAndServices = lines[7].split()[1:-1]
        # 支付给职工以及为职工支付的现金
        cashPaidToAndOnBehalfOfemployees = lines[8].split()[1:-1]
        # 支付的各项税费
        paymentsOfTaxesAndSurcharges = lines[9].split()[1:-1]
        # 支付的其他与经营活动有关的现金
        cashPaidRelatingToOtherOperatingActivities = lines[10].split()[1:-1]
        # 经营活动现金流出小计
        subTotalOfCashOutflowsFromOperatingActivities = lines[11].split()[1:-1]
        # 经营活动产生的现金流量净额
        netCashFlowsFromOperatingActivities = lines[12].split()[1:-1]
        # /*二、投资活动产生的现金流量*/
        # 收回投资所收到的现金
        cashReceivedFromDisposalOfInvestments = lines[14].split()[1:-1]
        # 取得投资收益所收到的现金
        cashReceivedFromReturnsOnIvestments = lines[15].split()[1:-1]
        # 处置固定资产、无形资产和其他长期资产所收回的现金净额
        netCashReceivedFromDisposalAssets = lines[16].split()[1:-1]
        # 处置子公司及其他营业单位收到的现金净额
        netCashReceivedFromDisposalSubsidiaries = lines[17].split()[1:-1]
        # 收到的其他与投资活动有关的现金
        cashReceivedFromOtherInvesting = lines[18].split()[1:-1]
        # 投资活动现金流入小计
        subTotalOfCashInflowsFromInvesting = lines[19].split()[1:-1]
        # 购建固定资产、无形资产和其他长期资产所支付的现金
        cashPaidToAcquireFixedAssets = lines[20].split()[1:-1]
        # 投资所支付的现金
        cashPaidToAcquireInvestments = lines[21].split()[1:-1]
        # 取得子公司及其他营业单位支付的现金净额
        netCashPaidToAcquireSubsidiaries = lines[22].split()[1:-1]
        # 支付的其他与投资活动有关的现金
        cashPaidRelatingToOtherInvesting = lines[23].split()[1:-1]
        # 投资活动现金流出小计
        subTotalOfCashOutflowsFromInvesting = lines[24].split()[1:-1]
        # 投资活动产生的现金流量净额
        netCashFlowsFromInvesting = lines[25].split()[1:-1]
        # /*三、筹资活动产生的现金流量*/
        # 吸收投资收到的现金
        cashReceivedFromCapitalContributions = lines[27].split()[1:-1]
        # 其中：子公司吸收少数股东投资收到的现金
        cashReceivedFromMinorityShareholdersOfSubsidiaries = lines[28].split()[1:-1]
        # 取得借款收到的现金
        cashReceivedFromBorrowings = lines[29].split()[1:-1]
        # 发行债券收到的现金
        cashReceivedFromIssuingBonds = lines[30].split()[1:-1]
        # 收到其他与筹资活动有关的现金
        cashReceivedRelatingToOtherFinancingActivities = lines[31].split()[1:-1]
        # 筹资活动现金流入小计
        subTotalOfCashInflowsFromFinancingActivities = lines[32].split()[1:-1]
        # 偿还债务支付的现金
        cashRepaymentsOfBorrowings = lines[33].split()[1:-1]
        # 分配股利、利润或偿付利息所支付的现金
        cashPaymentsForInterestExpensesAndDistributionOfDividendsOrProfits = lines[34].split()[1:-1]
        # 其中：子公司支付给少数股东的股利、利润
        cashPaymentsForDividendsOrProfitToMinorityShareholders = lines[35].split()[1:-1]
        # 支付其他与筹资活动有关的现金
        cashPaymentsRelatingToOtherFinancingActivities = lines[36].split()[1:-1]
        # 筹资活动现金流出小计
        subTotalOfCashOutflowsFromFinancingActivities = lines[37].split()[1:-1]
        # 筹资活动产生的现金流量净额
        netCashFlowsFromFinancingActivities = lines[38].split()[1:-1]
        # /*四、汇率变动对现金及现金等价物的影响*/
        effectOfForeignExchangeRate = lines[39].split()[1:-1]
        # /*五、现金及现金等价物净增加额*/
        netIncreaseInCash = lines[40].split()[1:-1]
        # 加:期初现金及现金等价物余额
        cashAtBeginningOfyear = lines[41].split()[1:-1]
        # /*六、期末现金及现金等价物余额*/
        cashAtEndOfyear = lines[42].split()[1:-1]
        # /*附注*/
        # 净利润
        netProfit = lines[44].split()[1:-1]
        # 少数股东权益
        minorityStockholderInterest = lines[45].split()[1:-1]
        # 未确认的投资损失
        unrealisedInvestmentLosses = lines[46].split()[1:-1]
        # 资产减值准备
        allowanceForAssetDevaluation = lines[47].split()[1:-1]
        # 固定资产折旧、油气资产折耗、生产性物资折旧
        depreciationOfFixedAssets = lines[48].split()[1:-1]
        # 无形资产摊销
        amorizationOfIntangibleAssets = lines[49].split()[1:-1]
        # 长期待摊费用摊销
        longTermDeferredExpenses = lines[50].split()[1:-1]
        # 待摊费用的减少
        decreaseOfDeferredExpenses = lines[51].split()[1:-1]
        # 预提费用的增加
        IncreaseOfwithholdingExpenses = lines[52].split()[1:-1]
        # 处置固定资产、无形资产和其他长期资产的损失
        lossOnDisposalOfFixedAssets = lines[53].split()[1:-1]
        # 固定资产报废损失
        lossOnFixedAssetsDamaged = lines[54].split()[1:-1]
        # 公允价值变动损失
        lossOnFairValueChange = lines[55].split()[1:-1]
        # 递延收益增加（减：减少）
        changeOnDeferredRevenue = lines[56].split()[1:-1]
        # 预计负债
        estimatedLiabilities = lines[57].split()[1:-1]
        # 财务费用
        financingExpenses = lines[58].split()[1:-1]
        # 投资损失
        investmentLoss = lines[59].split()[1:-1]
        # 递延所得税资产减少
        decreaseOnDeferredIncomeTaxAssets = lines[60].split()[1:-1]
        # 递延所得税负债增加
        increaseOnDeferredIncomeTaxLiabilities = lines[61].split()[1:-1]
        # 存货的减少
        decreaseInInventories = lines[62].split()[1:-1]
        # 经营性应收项目的减少
        decreaseInReceivablesUnderOperatingActivities = lines[63].split()[1:-1]
        # 经营性应付项目的增加
        increaseInReceivablesUnderOperatingActivities = lines[64].split()[1:-1]
        # 已完工尚未结算款的减少(减:增加)
        decreaseOnAmountDue = lines[65].split()[1:-1]
        # 已结算尚未完工款的增加(减:减少)
        increaseOnSettlementNotYetCompleted = lines[66].split()[1:-1]
        # 其他
        other = lines[67].split()[1:-1]
        # 经营活动产生现金流量净额
        netCashFlowFromOperatingActivities = lines[68].split()[1:-1]
        # 债务转为资本
        debtsTransferToCapital = lines[69].split()[1:-1]
        # 一年内到期的可转换公司债券
        oneYearDueConvertibleBonds = lines[70].split()[1:-1]
        # 融资租入固定资产
        financingRentToFixedAsset = lines[71].split()[1:-1]
        # 现金的期末余额
        cashAtTheEndOfPeriod = lines[72].split()[1:-1]
        # 现金的期初余额
        cashAtTheBeginningOfPeriod = lines[73].split()[1:-1]
        # 现金等价物的期末余额
        cashEquivalentsAtTheEndOfPeriod = lines[74].split()[1:-1]
        # 现金等价物的期初余额
        cashEquivalentsAtTheBeginningOfPeriod = lines[75].split()[1:-1]
        # 现金及现金等价物的净增加额
        netIncreaseInCashAndCashEquivalents = lines[76].split()[1:-1]
    for idx, _ in enumerate(reportDate):
        yield {
            "reportDate": reportDate[idx],
            "securityId": security_item["id"],
            "code": security_item["code"],
            # /*一、经营活动产生的现金流量*/
            # 销售商品、提供劳务收到的现金
            "cashFromSellingCommoditiesOrOfferingLabor": cashFromSellingCommoditiesOrOfferingLabor[idx],
            # 收到的税费返还
            "refundOfTaxAndFeeReceived": refundOfTaxAndFeeReceived[idx],
            # 收到的其他与经营活动有关的现金
            "cashReceivedRelatingToOtherOperatingActivities": cashReceivedRelatingToOtherOperatingActivities[idx],
            # 经营活动现金流入小计
            "subTotalOfCashInflowsFromOperatingActivities": subTotalOfCashInflowsFromOperatingActivities[idx],
            # 购买商品、接受劳务支付的现金
            "cashPaidForGoodsAndServices": cashPaidForGoodsAndServices[idx],
            # 支付给职工以及为职工支付的现金
            "cashPaidToAndOnBehalfOfemployees": cashPaidToAndOnBehalfOfemployees[idx],
            # 支付的各项税费
            "paymentsOfTaxesAndSurcharges": paymentsOfTaxesAndSurcharges[idx],
            # 支付的其他与经营活动有关的现金
            "cashPaidRelatingToOtherOperatingActivities": cashPaidRelatingToOtherOperatingActivities[idx],
            # 经营活动现金流出小计
            "subTotalOfCashOutflowsFromOperatingActivities": subTotalOfCashOutflowsFromOperatingActivities[idx],
            # 经营活动产生的现金流量净额
            "netCashFlowsFromOperatingActivities": netCashFlowsFromOperatingActivities[idx],
            # /*二、投资活动产生的现金流量*/
            # 收回投资所收到的现金
            "cashReceivedFromDisposalOfInvestments": cashReceivedFromDisposalOfInvestments[idx],
            # 取得投资收益所收到的现金
            "cashReceivedFromReturnsOnIvestments": cashReceivedFromReturnsOnIvestments[idx],
            # 处置固定资产、无形资产和其他长期资产所收回的现金净额
            "netCashReceivedFromDisposalAssets": netCashReceivedFromDisposalAssets[idx],
            # 处置子公司及其他营业单位收到的现金净额
            "netCashReceivedFromDisposalSubsidiaries": netCashReceivedFromDisposalSubsidiaries[idx],
            # 收到的其他与投资活动有关的现金
            "cashReceivedFromOtherInvesting": cashReceivedFromOtherInvesting[idx],
            # 投资活动现金流入小计
            "subTotalOfCashInflowsFromInvesting": subTotalOfCashInflowsFromInvesting[idx],
            # 购建固定资产、无形资产和其他长期资产所支付的现金
            "cashPaidToAcquireFixedAssets": cashPaidToAcquireFixedAssets[idx],
            # 投资所支付的现金
            "cashPaidToAcquireInvestments": cashPaidToAcquireInvestments[idx],
            # 取得子公司及其他营业单位支付的现金净额
            "netCashPaidToAcquireSubsidiaries": netCashPaidToAcquireSubsidiaries[idx],
            # 支付的其他与投资活动有关的现金
            "cashPaidRelatingToOtherInvesting": cashPaidRelatingToOtherInvesting[idx],
            # 投资活动现金流出小计
            "subTotalOfCashOutflowsFromInvesting": subTotalOfCashOutflowsFromInvesting[idx],
            # 投资活动产生的现金流量净额
            "netCashFlowsFromInvesting": netCashFlowsFromInvesting[idx],
            # /*三、筹资活动产生的现金流量*/
            # 吸收投资收到的现金
            "cashReceivedFromCapitalContributions": cashReceivedFromCapitalContributions[idx],
            # 其中：子公司吸收少数股东投资收到的现金
            "cashReceivedFromMinorityShareholdersOfSubsidiaries": cashReceivedFromMinorityShareholdersOfSubsidiaries[
                idx],
            # 取得借款收到的现金
            "cashReceivedFromBorrowings": cashReceivedFromBorrowings[idx],
            # 发行债券收到的现金
            "cashReceivedFromIssuingBonds": cashReceivedFromIssuingBonds[idx],
            # 收到其他与筹资活动有关的现金
            "cashReceivedRelatingToOtherFinancingActivities": cashReceivedRelatingToOtherFinancingActivities[idx],
            # 筹资活动现金流入小计
            "subTotalOfCashInflowsFromFinancingActivities": subTotalOfCashInflowsFromFinancingActivities[idx],
            # 偿还债务支付的现金
            "cashRepaymentsOfBorrowings": cashRepaymentsOfBorrowings[idx],
            # 分配股利、利润或偿付利息所支付的现金
            "cashPaymentsForInterestExpensesAndDistributionOfDividendsOrProfits":
                cashPaymentsForInterestExpensesAndDistributionOfDividendsOrProfits[idx],
            # 其中：子公司支付给少数股东的股利、利润
            "cashPaymentsForDividendsOrProfitToMinorityShareholders":
                cashPaymentsForDividendsOrProfitToMinorityShareholders[idx],
            # 支付其他与筹资活动有关的现金
            "cashPaymentsRelatingToOtherFinancingActivities": cashPaymentsRelatingToOtherFinancingActivities[idx],
            # 筹资活动现金流出小计
            "subTotalOfCashOutflowsFromFinancingActivities": subTotalOfCashOutflowsFromFinancingActivities[idx],
            # 筹资活动产生的现金流量净额
            "netCashFlowsFromFinancingActivities": netCashFlowsFromFinancingActivities[idx],
            # /*四、汇率变动对现金及现金等价物的影响*/
            "effectOfForeignExchangeRate": effectOfForeignExchangeRate[idx],
            # /*五、现金及现金等价物净增加额*/
            "netIncreaseInCash": netIncreaseInCash[idx],
            # 加:期初现金及现金等价物余额
            "cashAtBeginningOfyear": cashAtBeginningOfyear[idx],
            # /*六、期末现金及现金等价物余额*/
            "cashAtEndOfyear": cashAtEndOfyear[idx],
            # /*附注*/
            # 净利润
            "netProfit": netProfit[idx],
            # 少数股东权益
            "minorityStockholderInterest": minorityStockholderInterest[idx],
            # 未确认的投资损失
            "unrealisedInvestmentLosses": unrealisedInvestmentLosses[idx],
            # 资产减值准备
            "allowanceForAssetDevaluation": allowanceForAssetDevaluation[idx],
            # 固定资产折旧、油气资产折耗、生产性物资折旧
            "depreciationOfFixedAssets": depreciationOfFixedAssets[idx],
            # 无形资产摊销
            "amorizationOfIntangibleAssets": amorizationOfIntangibleAssets[idx],
            # 长期待摊费用摊销
            "longTermDeferredExpenses": longTermDeferredExpenses[idx],
            # 待摊费用的减少
            "decreaseOfDeferredExpenses": decreaseOfDeferredExpenses[idx],
            # 预提费用的增加
            "IncreaseOfwithholdingExpenses": IncreaseOfwithholdingExpenses[idx],
            # 处置固定资产、无形资产和其他长期资产的损失
            "lossOnDisposalOfFixedAssets": lossOnDisposalOfFixedAssets[idx],
            # 固定资产报废损失
            "lossOnFixedAssetsDamaged": lossOnFixedAssetsDamaged[idx],
            # 公允价值变动损失
            "lossOnFairValueChange": lossOnFairValueChange[idx],
            # 递延收益增加（减：减少）
            "changeOnDeferredRevenue": changeOnDeferredRevenue[idx],
            # 预计负债
            "estimatedLiabilities": estimatedLiabilities[idx],
            # 财务费用
            "financingExpenses": financingExpenses[idx],
            # 投资损失
            "investmentLoss": investmentLoss[idx],
            # 递延所得税资产减少
            "decreaseOnDeferredIncomeTaxAssets": decreaseOnDeferredIncomeTaxAssets[idx],
            # 递延所得税负债增加
            "increaseOnDeferredIncomeTaxLiabilities": increaseOnDeferredIncomeTaxLiabilities[idx],
            # 存货的减少
            "decreaseInInventories": decreaseInInventories[idx],
            # 经营性应收项目的减少
            "decreaseInReceivablesUnderOperatingActivities": decreaseInReceivablesUnderOperatingActivities[idx],
            # 经营性应付项目的增加
            "increaseInReceivablesUnderOperatingActivities": increaseInReceivablesUnderOperatingActivities[idx],
            # 已完工尚未结算款的减少(减:增加)
            "decreaseOnAmountDue": decreaseOnAmountDue[idx],
            # 已结算尚未完工款的增加(减:减少)
            "increaseOnSettlementNotYetCompleted": increaseOnSettlementNotYetCompleted[idx],
            # 其他
            "other": other[idx],
            # 经营活动产生现金流量净额
            "netCashFlowFromOperatingActivities": netCashFlowFromOperatingActivities[idx],
            # 债务转为资本
            "debtsTransferToCapital": debtsTransferToCapital[idx],
            # 一年内到期的可转换公司债券
            "oneYearDueConvertibleBonds": oneYearDueConvertibleBonds[idx],
            # 融资租入固定资产
            "financingRentToFixedAsset": financingRentToFixedAsset[idx],
            # 现金的期末余额
            "cashAtTheEndOfPeriod": cashAtTheEndOfPeriod[idx],
            # 现金的期初余额
            "cashAtTheBeginningOfPeriod": cashAtTheBeginningOfPeriod[idx],
            # 现金等价物的期末余额
            "cashEquivalentsAtTheEndOfPeriod": cashEquivalentsAtTheEndOfPeriod[idx],
            # 现金等价物的期初余额
            "cashEquivalentsAtTheBeginningOfPeriod": cashEquivalentsAtTheBeginningOfPeriod[idx],
            # 现金及现金等价物的净增加额
            "netIncreaseInCashAndCashEquivalents": netIncreaseInCashAndCashEquivalents[idx]
        }


if __name__ == '__main__':
    for item in get_cash_flow_statement_items(
            SecurityItem(type='stock', code='000004', exchange='sz', id='stock_sz_000004')):
        print(item)
