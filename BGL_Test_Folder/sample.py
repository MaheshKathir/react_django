# Pypdf FileReader and Writer getting  Deprecated Error means install this  -> pip install 'PyPDF2<3.0'
# To Resolve the fitz error , need to install this pymupdf                  -> pip install pymupdf
# for pip                                                                   -> py -m pip


#Modules or libraries for this project

import pdfplumber
import re
import fitz
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from os import path
import os

#this module for mask the input text 
import pwinput


def pdf_automation():

    #For password functionality
    password_list  = ['!@#$%12345','1111']
    password = input("Password: ")

    if password in password_list:

        path_folder = 'C:\BGL_Test_Folder'

        for root, dirs, files in os.walk(path_folder):
            for pdf_file in files:
                pdf_path = path.join(root, pdf_file)

                #Defined Words to search into the PDF file
                

                # words_to_find = ['Unsettle Trade', 'Dividends Receivable', 'Distributions Receivable','PAYG Payable',
                #                  'Interest Received','Employer Contributions','Personal Non Concessional','Accountancy Fees','ATO Supervisory Levy',
                #                  'Investment Expenses','Changes in Market Values','Benefits accrued as a result of operations before income tax','Income Tax Expense','Dividends Received','Trust Distributions','Income Tax Payable',
                #                  'Shares in Listed Companies', 'Units in Listed Unit Trusts', 'Managed Investments', 'ANZ - E*trade Cash Investment Account', 'CBA Direct Investment Account']
                # words_to_find = ['Benefits accrued as a result of operations before income tax', 'Income Tax Expense','Changes in Market Values']
                
                words_to_find = [

                                    'Managed Investments (Australian)',
                                    'Managed Investments (Overseas)',
                                    'Shares in Listed Companies (Australian)',
                                    'Shares in Listed Companies (Overseas)',	
                                    'Shares in Unlisted Private Companies (Overseas)',
                                    'Units in Listed Unit Trusts (Australian)',
                                    'Units in Unlisted Unit Trusts (Australian)',
                                    'Plant and Equipment (at written down value) - Unitised',
                                    'Real Estate Properties ( Australian - Residential)',
                                    'Derivatives (Options, Hybrids, Future Contracts)',
                                    'Other Assets',
                                    'Loans to Associated Entities (In house loans) - Unitised',
                                    'Stapled Securities',
                                    'Mortgage Loans (Australian)',
                                    'Fixed Interest Securities (Australian) - Unitised',
                                    'Shares in Unlisted Private Companies (Australian)',
                                    'Units in Listed Trusts (Australian)',
                                
                                    'Sundry Debtors',
                                    'ANZ - Premium Cash Account',
                                    'ANZ - E*trade Cash Investment Account',
                                    'SMA - Cash Account',
                                    'Unsettle Trade',
                                    'Dividends Receivable',
                                    'CBA Direct Investment Account',
                                    'Distributions Receivable',
                                    'Income Tax Refundable',
                                    'Deferred Tax Liability'

                                    'Income Tax Payable',
                                    'PAYG Payable',
                                    'Sundry Creditors',
                                    'Amounts owing to other persons',

                                    'Trust Distributions',
                                    'Dividends Received',
                                    'Interest Received',
                                    'Other Investment Income',
                                    'Property Income',

                                    'Employer Contributions',
                                    'Personal Concessional',
                                    'Personal Non Concessional',

                                    'Forex Gain/Loss',
                                    'Life Insurance Premiums',

                                    'Accountancy Fees',
                                    'ATO Supervisory Levy',
                                    'Investment Expenses',
                                    "Auditor's Remuneration",
                                    'ASIC Fees',
                                    'Forex Exchange Loss',
                                    'Other Expenses',
                                    'Other Expenses - Non deductible',
                                    'Bank Charges',
                                    'Depreciation',
                                    'Interest Paid',
                                    'Property Expenses - Agents Management Fees',
                                    'Property Expenses - Council Rates',
                                    'Property Expenses - Insurance Premium',
                                    'Property Expenses - Repairs Maintenance',
                                    'Property Expenses - Sundry Expenses',
                                    'Property Expenses - Water Rates',
                                    'Administration Costs',
                                    'Investment Expenses',
                                    'Unsettled Trades',

                                    'Benefits accrued as a result of operations before income tax',
                                    'Income Tax Expense',

                                    'Pensions Paid',
                                    'Benefits Paid/Transfers Out',
                                    'Refund Excess Contributions',

                                    'Changes in Market Values',

    'BHP Group Limited',
    'Commonwealth Bank of Australia','CSL Limited','National Australia Bank Limited','Westpac Banking Corporation','ANZ Group Holdings Limited',
    'Woodside Energy Group Limited','Macquarie Group Limited','Fortescue Metals Group Limited','Wesfarmers Limited','Woolworths Group Limited',
    'Telstra Group Limited','Goodman Group','Transurban Group','RIO Tinto Limited','Aristocrat Leisure Limited','Santos Limited','Wisetech Global Limited',
    'Newcrest Mining Limited','QBE Insurance Group Limited','Coles Group Limited','REA Group Limited','Brambles Limited','James Hardie Industries Plc',
    'Xero Limited','Cochlear Limited','Suncorp Group Limited','SOUTH32 Limited','Sonic Healthcare Limited','Computershare Limited','Origin Energy Limited',
    'Scentre Group','Insurance Australia Group Limited','Pilbara Minerals Limited','Mineral Resources Limited','Northern Star Resources Limited','Reece Limited',
    'Vanguard Australian Shares INDEX ETF','Fisher & Paykel Healthcare Corporation Limited','Ramsay Health Care Limited','Washington H Soul Pattinson & Company Limited',
    'ASX Limited','The Lottery Corporation Limited','APA Group','Resmed Inc','Auckland International Airport Limited','Carsales.com Limited','Qantas Airways Limited',
    'TPG Telecom Limited','Seven Group Holdings Limited','Stockland','IGO Limited','Endeavour Group Limited','Medibank Private Limited','Amcor Plc','Gold Corporation',
    'Bluescope Steel Limited','Mirvac Group','Worley Limited','Allkem Limited','Atlas Arteria','Treasury Wine Estates Limited','Australian Foundation Investment Company Limited',
    'Spark New Zealand Limited','Vicinity Centres','Dexus','Seek Limited','Ampol Limited','Mercury NZ Limited','GPT Group','Pro Medicus Limited','Infratil Limited',
    'AGL Energy Limited','Orica Limited','Yancoal Australia Limited','Idp Education Limited','Magellan Global Fund (Open Class) (Managed Fund)','NEXTDC Limited',
    'Lynas Rare EARTHS Limited','Evolution Mining Limited','Aurizon Holdings Limited','Ebos Group Limited','Argo Investments Limited','Meridian Energy Limited',
    'Altium Limited','Vanguard MSCI INDEX International Shares ETF','Ishares S&P 500 ETF','Liontown Resources Limited','Cleanaway Waste Management Limited','Steadfast Group Limited',
    'Incitec Pivot Limited','Als Limited','Whitehaven Coal Limited','QUBE Holdings Limited','Bendigo and Adelaide Bank Limited','Lendlease Group','Boral Limited',
    'Charter Hall Group','JB Hi-Fi Limited','Technology One Limited','New Hope Corporation Limited','Viva Energy Group Limited',"Domino's PIZZA Enterprises Limited",
    'SPDR S&P/ASX 200 Fund','Harvey Norman Holdings Limited','Challenger Limited','Flight Centre Travel Group Limited','GQG Partners Inc','Ishares Core S&P/ASX 200 ETF',
    'Premier Investments Limited','Brickworks Limited','Eagers Automotive Limited','Vaneck MSCI International Quality ETF','Nib Holdings Limited','Bank of Queensland Limited',
    'Netwealth Group Limited','Metcash Limited','Vanguard US Total Market Shares INDEX ETF','Iluka Resources Limited','Beach Energy Limited','Fletcher Building Limited',
    'TELIX Pharmaceuticals Limited','AMP Limited','Breville Group Limited','Betashares Nasdaq 100 ETF','The a2 Milk Company Limited','AUB Group Limited','Nine Entertainment Co. Holdings Limited',
    'Reliance Worldwide Corporation Limited','Chorus Limited','Betashares Australia 200 ETF','National Storage REIT','Champion Iron Limited','Betashares Australian High Interest Cash ETF',
    'Alumina Limited','Ansell Limited','Global X Metal Securities Australia Limited','Vanguard Australian Shares High Yield ETF','Orora Limited','Sandfire Resources Limited',
    'Sims Limited','Super Retail Group Limited','Ishares Global 100 ETF','Webjet Limited','Downer Edi Limited','CSR Limited','ARB Corporation Limited',
    'Corporate Travel Management Limited','Block Inc','AVZ Minerals Limited','Zimplats Holdings Limited','Nickel Industries Limited','Coronado Global Resources Inc',
    'Vanguard All-World Ex-US Shares INDEX ETF','Betashares Global Sustainability Leaders ETF','HUB24 Limited','Stanmore Resources Limited','Perseus Mining Limited',
    'Charter Hall Long Wale REIT','BSP Financial Group Limited','Homeco Daily Needs REIT','Tabcorp Holdings Limited','Paladin Energy Limited','Magellan Global Fund',
    'National Australia Bank Limited','Region Group','Air New Zealand Limited','Vanguard Australian Property Securities INDEX ETF','Vanguard MSCI INDEX International Shares (Hedged) ETF',
    'Lovisa Holdings Limited','Perpetual Limited','Genesis Energy Limited','Domain Holdings Australia Limited','BWP Trust','Ventia Services Group Limited',
    'Hyperion GBL Growth Companies Fund (Managed Fund)','Deterra Royalties Limited','Bapcor Limited','De Grey Mining Limited','Virgin Money Uk Plc',
    'Summerset Group Holdings Limited','Vanguard Diversified High Growth INDEX ETF','Pexa Group Limited','National Australia Bank Limited','Ishares Core Composite Bond ETF',
    'Betashares Active Australian Hybrids Fund (Managed Fund)','Charter Hall Retail REIT','Nufarm Limited','National Australia Bank Limited','Centuria Industrial REIT',
    'EVT Limited','Contact Energy Limited','Gold Road Resources Limited','Vaneck Australian EQUAL Weight ETF','HMC Capital Limited','Megaport Limited',
    'Pinnacle Investment Management Group Limited','Bellevue Gold Limited','Wam Leaders Limited','Growthpoint Properties Australia','Lifestyle Communities Limited',
    'WAM Capital Limited','IPH Limited','Invocare Limited','L1 Long Short Fund Limited','Commonwealth Bank of Australia','LIFE360 Inc','Metrics Master Income Trust',
    'Westpac Banking Corporation','PSC Insurance Group Limited','Westpac Banking Corporation','Commonwealth Bank of Australia','Johns LYNG Group Limited',
    'Kelsian Group Limited','Westpac Banking Corporation','MFF Capital Investments Limited','Magellan Financial Group Limited','Graincorp Limited',
    'APM Human Services International Limited','G.U.D. Holdings Limited','Waypoint REIT','Insignia Financial Limited','Commonwealth Bank of Australia','Capricorn Metals Limited',
    'Ingenia Communities Group','Australia and New Zealand Banking Group Limited','Genesis Minerals Limited','Healius Limited','Abacus Storage King','Vanguard Australian Fixed Interest INDEX ETF',
    'The Star Entertainment Group Limited','Neuren Pharmaceuticals Limited','Commonwealth Bank of Australia','Macquarie Technology Group Limited','Dicker Data Limited',
    'Skycity Entertainment Group Limited','Commonwealth Bank of Australia','Mader Group Limited','Westpac Banking Corporation','Australia and New Zealand Banking Group Limited',
    'Australia and New Zealand Banking Group Limited','United Malt Group Limited','Westpac Banking Corporation','Chalice Mining Limited','Credit Corp Group Limited',
    'Adbri Limited','Commonwealth Bank of Australia','Codan Limited','BKI Investment Company Limited','Monadelphous Group Limited','Emerald Resources NL',
    'Dalrymple Bay Infrastructure Limited','Light & Wonder Inc','Ramelius Resources Limited','Karoon Energy Limited','REDOX Limited','Costa Group Holdings Limited',
    'Ishares Global Healthcare ETF','Australia and New Zealand Banking Group Limited','Siteminder Limited','Arena REIT','Inghams Group Limited','Cromwell Property Group',
    'Nanosonics Limited','Sayona Mining Limited','Resolution Cap Global Prop Sec (Managed Fund)','Betashares Australian Sustainability Leaders ETF','Mcmillan Shakespeare Limited',
    'NRW Holdings Limited','Latitude Group Holdings Limited','Regis Resources Limited','Iress Limited','Australian United Investment Company Limited','Centuria Capital Group',
    'Helia Group Limited','Objective Corporation Limited','Commonwealth Bank of Australia','Boss Energy Limited','Accent Group Limited','Liberty Financial Group',
    'Collins Foods Limited','Ishares S&P 500 Aud Hedged ETF','Data#3 Limited','Heartland Group Holdings Limited','Betashares Australian Bank Senior Floating Rate Bond ETF',
    'Leo Lithium Limited','Smartgroup Corporation Limited','Hansen Technologies Limited','Audinate Group Limited','Maas Group Holdings Limited','PWR Holdings Limited',
    'Cettire Limited','Abacus Group','AZURE Minerals Limited','Charter Hall Social Infrastructure REIT','Macquarie Group Limited','Diversified United Investment Limited',
    'Elders Limited','Polynovo Limited','Judo Capital Holdings Limited','Vulcan Steel Limited','Nick Scali Limited','Jumbo Interactive Limited','Briscoe Group Australasia Limited',
    'Clinuvel Pharmaceuticals Limited','Strike Energy Limited','Australia and New Zealand Banking Group Limited','Macquarie Group Limited','National Australia Bank Limited',
    'SG Fleet Group Limited','Vanguard Australian Government Bond INDEX ETF','News Corporation','G8 Education Limited','Tuas Limited','Bega Cheese Limited',
    'Silver Lake Resources Limited','Energy Resources of Australia Limited','Dexus Industria REIT','Platinum Asset Management Limited','Ishares MSCI Emerging Markets ETF',
    'Aussie Broadband Limited','West African Resources Limited','Adriatic Metals Plc','Alpha Hpa Limited','Australian Agricultural Company Limited','Vanguard International Fixed Interest INDEX (Hedged) ETF',
    'Vaneck Australian Subordinated Debt ETF','Sigma Healthcare Limited','Core Lithium Limited','Temple & Webster Group Limited','Latin Resources Limited',
    'Healthco Healthcare and Wellness REIT','SPDR S&P/ASX 50 Fund','Ma Financial Group Limited','IMDEX Limited','Rural Funds Group','Vaneck Ftse Global Infrastructure (Hedged) ETF',
    'Resolute Mining Limited','Ooh!Media Limited','Vanguard Global Aggregate Bond INDEX (Hedged) ETF','Plato Income Maximiser Limited','RED 5 Limited','Ishares Europe ETF',
    'Vanguard MSCI Australian Small Companies INDEX ETF','Estia Health Limited','Carlton Investments Limited','PM Capital Global Opportunities Fund Limited','Westgold Resources Limited',
    'Macquarie Group Limited','Centuria Office REIT','Fleetpartners Group Limited','Tourism Holdings Rentals Limited','Betashares Global Cybersecurity ETF',
    'Activex Ardea Real Outcome Bond Fund (Managed Fund)','Weebit Nano Limited','Regis Healthcare Limited','SILEX Systems Limited','Djerriwarrh Investments Limited',
    'Macquarie Group Limited','Vanguard Ftse Emerging Markets Shares ETF','Nanuk New World Fund (Managed Fund)','Tyro Payments Limited','Vanguard Ethically Conscious International Shares INDEX ETF',
    'Vaneck MSCI International Quality (Hedged) ETF','CALIX Limited','Ishares Asia 50 ETF','Winton Land Limited','EQT Holdings Limited','Perenti Limited','Integral Diagnostics Limited',
    'Vanguard Diversified Growth INDEX ETF','Qualitas Limited','Wam Global Limited','Ishares Core MSCI World Ex Australia Esg ETF','Austal Limited','Macquarie Bank Limited',
    'Ishares Core Cash ETF','Magellan Infrastructure Fund (Currency Hedged)(Managed Fund)','Fineos Corporation Holdings Plc','Ridley Corporation Limited','Link Administration Holdings Limited',
    'Deep Yellow Limited','Unibail-Rodamco-Westfield','Macquarie Bank Limited','KKR Credit Income Fund','Vaneck Morningstar Wide Moat ETF','Infomedia Limited',
    'Vanguard Australian Corp Fixed Interest INDEX ETF','Vanguard Diversified Balanced INDEX ETF','Regal Partners Limited','Vaneck Australian Floating Rate ETF',
    'Vaneck Australian Property ETF','NB Global Corporate Income Trust','Global X Battery Tech & Lithium ETF','Supply Network Limited','Ishares Government Inflation ETF',
    'Omni Bridgeway Limited','Australian Clinical Labs Limited','Qualitas Real Estate Income Fund','Whitefield Industrials Limited','Hotel Property Investments',
    'Pepper Money Limited','Vanguard Global Value Equity Active ETF (Managed Fund)','Vulcan Energy Resources Limited','Regal Investment Fund','Peet Limited',
    'Hutchison Telecommunications (Australia) Limited','Pacific Current Group Limited','Kogan.com Limited','Cobram Estate Olives Limited','Service Stream Limited',
    'Mirrabooka Investments Limited','Ophir High Conviction Fund','Hearts and Minds Investments Limited','Develop Global Limited','Betashares Australian Investment Grade Corporate Bond ETF',
    'KMD Brands Limited','Myer Holdings Limited','Metrics Income Opportunities Trust','Novonix Limited','Tietto Minerals Limited','Brainchip Holdings Limited',
    'Restaurant Brands New Zealand Limited','Arafura Rare EARTHS Limited','Mount Gibson Iron Limited','Vgi Partners Global Investments Limited','Ishares S&P/ASX 20 ETF',
    'GWA Group Limited','Propel Funeral Partners Limited','Autosports Group Limited','Global X US Treasury Bond ETF (Currency Hedged)','Bendigo and Adelaide Bank Limited','Grange Resources Limited',
    'Alliance Aviation Services Limited','Insurance Australia Group Limited','Helloworld Travel Limited','NUIX Limited','Select Harvests Limited','Mma Offshore Limited',
    'Oceania Healthcare Limited','Betashares Westn Asset Aus Bond Fund (Managed Fund)','Pointsbet Holdings Limited','Australian Ethical Investment Limited','Ishares MSCI Japan ETF',
    'SPDR S&P/ASX 200 Listed Property Fund','Ioneer Limited','Gryphon Capital Income Trust','Betashares Asia Technology Tigers ETF','Monash Ivf Group Limited',
    'Betashares Australian Government Bond ETF','Partners Group Global Income Fund','Future Generation Australia Limited','Future Generation Global Limited','Ishares S&P Small-Cap ETF',
    'Perpetual Equity Investment Company Limited','Seven West Media Limited','Betashares Gold Bullion ETF - Currency Hedged','Magellan High Conviction Trust (Managed Fund)',
    'Talga Group Limited','Betashares Ftse 100 ETF','Imugene Limited','Patriot Battery Metals Inc','Peter Warren Automotive Holdings Limited','OFX Group Limited','Boart Longyear Group Limited',
    'Vaneck Gold Miners ETF','Predictive Discovery Limited','Betashares Ftse Rafi Australia 200 ETF','Ricegrowers Limited','Cedar Woods Properties Limited','Alphinity Global Equity Fund (Managed Fund)',
    'Serko Limited','SSR Mining Inc','Pengana Private Equity Trust','Resimac Group Limited','Ishares MSCI Eafe ETF','SPDR Dow Jones Global Real Estate Esg Fund',
    'Gentrack Group Limited','Ishares Treasury ETF','Australian Finance Group Limited','Delta Lithium Limited','Perpetual Credit Income Trust','Suncorp Group Limited',
    'Alkane Resources Limited','Beacon Lighting Group Limited','Lycopodium Limited','Mayne Pharma Group Limited','Bank of Queensland Limited','EML Payments Limited',
    'Betashares Aus Top 20 Equity Yield MAX Fund (Managed Fund)','Readytech Holdings Limited','Challenger Limited','SPDR MSCI Australia Select High Dividend Yield Fund',
    'Suncorp Group Limited','GR Engineering Services Limited','Betashares Geared Australian Equity Fund (Hedge Fund)','Platinum Capital Limited','Om Holdings Limited',
    'Airlie Australian Share Fund (Managed Fund)','Chrysos Corporation Limited','Betashares Global Quality Leaders ETF','Argo Global Listed Infrastructure Limited',
    'Janus Henderson Group Plc','Vanguard Ethically Conscious Australian Shares ETF','Global Lithium Resources Limited','Vaneck Australian Resources ETF',
    'Suncorp Group Limited','Ipd Group Limited','Jupiter Mines Limited','Syrah Resources Limited','Meteoric Resources NL','Regal Asian Investments Limited',
    'Betashares Global Sustainability Leaders ETF - CH','Ram Essential Services Property Fund','Lindsay Australia Limited','Mesoblast Limited','Centaurus Metals Limited',
    'SRG Global Limited','Smartpay Holdings Limited','Terracom Limited','SPDR S&P Global Dividend Fund','Clearview Wealth Limited','Steamships Trading Company Limited',
    'Vanguard Global Infrastructure INDEX ETF','29METALS Limited','Challenger Limited','Mystate Limited','Macmahon Holdings Limited','Renascor Resources Limited',
    'Bank of Queensland Limited','Aft Pharmaceuticals Limited','Vanguard Ftse Asia Ex Japan Shares INDEX ETF','Impedimed Limited','Michael Hill International Limited',
    'Antipodes Global Shares (Quoted Managed Fund)','Vista Group International Limited','Dexus Convenience Retail REIT','Kingsgate Consolidated Limited','BCI Minerals Limited',
    'Bravura Solutions Limited','Navigator Global Investments Limited','Superloop Limited','Rpmglobal Holdings Limited','DDH1 Limited','SPDR S&P World Ex Australia Carbon Control Fund',
    'Bell Financial Group Limited','Emeco Holdings Limited','Duratec Limited','Argosy Minerals Limited','Ainsworth Game Technology Limited','K & S Corporation Limited',
    'Global X Fang+ ETF','Lindian Resources Limited','GDI Property Group','Anteris Technologies Limited','Praemium Limited','Wam Microcap Limited','Global X Morningstar Global Technology ETF',
    'Immutep Limited','Bendigo and Adelaide Bank Limited','Sky Network Television Limited','Platinum International Fund (Quoted Managed Hedge Fund)','WCM Quality Global Growth Fund (Quoted Managed Fund)',
    'Ive Group Limited','Aspen Group','Russell Investments Australian Responsible Investment ETF','Ishares Global 100 Aud Hedged ETF','Ishares China Large-Cap ETF',
    'Avita Medical Inc',"Fonterra Shareholders' Fund",'Burgundy Diamond Mines Limited','Carindale Property Trust','3P Learning Limited','Platinum Asia Investments Limited',
    'Lake Resources N.L.','Amcil Limited','Cooper Energy Limited','Audio Pixels Holdings Limited','Aroa Biosurgery Limited','Lotus Resources Limited','Bannerman Energy Limited',
    'Universal Store Holdings Limited','Servcorp Limited','Ishares S&P/ASX DIV Opportunities Esg Screened ETF','AMP Limited','Australian Unity Limited','United Overseas Australia Limited',
    'Baby Bunting Group Limited','Australian Strategic Materials Limited','Neometals Limited','QORIA Limited','Botanix Pharmaceuticals Limited',
    'Turners Automotive Group Limited','Lynch Group Holdings Limited','ZIP Co Limited','CVC Limited','Betashares Sustainability Leaders DVRSFD Bond ETF - Cur HDG',
    'Carnarvon Energy Limited','Betashares Australian Strong Bear (Hedge Fund)','4DS Memory Limited','Ishares Edge MSCI World Minimum Volatility ETF',
    'Betashares Nasdaq 100 ETF - Currency Hedged','Clarity Pharmaceuticals Limited','Pengana International Equities Limited','Synlait Milk Limited',
    'Red Hill Minerals Limited','Ramsay Health Care Limited','Betashares Australian Major Bank Hybrids INDEX ETF','Catapult Group International Limited',
    'Bank of Queensland Limited','Arn Media Limited','Ardent Leisure Group Limited','Solvar Limited','Garda Property Group','Vaneck Australian Corporate Bond Plus ETF',
    'Pantoro Limited','Generation Development Group Limited','Vanguard MSCI International Small Companies INDEX ETF','Piedmont Lithium Inc','Strandline Resources Limited',
    'Russell Investments Australian Select Corporate Bond ETF','Betashares Diversified All Growth ETF','Galan Lithium Limited','Greenx Metals Limited',
    'Bigtincan Holdings Limited','COG Financial Services Limited','Ishares Enhanced Cash ETF','EBR Systems Inc','Spartan Resources Limited','Metals X Limited',
    'Sovereign Metals Limited','Base Resources Limited','Melbana Energy Limited','Duxton Water Limited','Auswide Bank Limited','Adairs Limited','Horizon Oil Limited',
    'Brockman Mining Limited','Ishares S&P Mid-Cap ETF','Appen Limited','Tamboran Resources Limited','Betashares US EQY Strong Bear - CH (Hedge Fund)',
    'Winsome Resources Limited','Russell Investments High Dividend Australian Shares ETF','Cogstate Limited','Silver Mines Limited','DGL Group Limited',
    'Atlantic Lithium Limited','Loftus Peak Global Disruption Fund (Managed Fund)','Elanor Commercial Property Fund','Wildcat Resources Limited',
    'Acrow Formwork and Construction Services Limited','Pact Group Holdings Limited','Betashares Australian Ex-20 Portfolio Diversifier ETF','Ishares Core Global Corporate Bond(Aud Hedged) ETF',
    'Vaneck Ftse International Property (Hedged) ETF','Vanguard Ftse Europe Shares ETF','Global X Robo Global Robotics & Automation ETF','Betashares Australian Composite Bond ETF',
    'Schaffer Corporation Limited','Firefinch Limited','Cyclopharm Limited','Orecorp Limited','Nufarm Finance (NZ) Limited','Ishares Core MSCI World Ex Aus Esg (Aud Hed) ETF',
    'Wam Research Limited','WCM Global Growth Limited','Kina Securities Limited','Capitol Health Limited','Betashares S&P 500 EQUAL Weight ETF','Close the Loop Limited',
    'Pacific Smiles Group Limited','Elanor Investors Group','Trajan Group Holdings Limited','Cadence Capital Limited','Iperionx Limited','Humm Group Limited',
    '4DMEDICAL Limited','Bowen Coking Coal Limited','PYC Therapeutics Limited','US Masters Residential Property Fund','Civmec Limited','Tower Limited',
    'Vitura Health Limited','Fidelity Global Emerging Markets Fund (Managed Fund)','Probiotec Limited','Ishares Global Consumer Staples ETF','Musgrave Minerals Limited',
    'Australian Unity Office Fund','The Reject Shop Limited','Vanguard Diversified Conservative INDEX ETF','Peoplein Limited','Magnetic Resources NL','QV Equities Limited',
    'WA1 Resources Limited','Newmark Property REIT','Southern Cross Electrical Engineering Limited','Betashares Global Energy Companies ETF - Currency Hedged',
    'SYMBIO Holdings Limited','DUG Technology Limited','Wam Alternative Assets Limited','SPDR S&P World Ex Aus Carbon Control (Hedged) Fund','Kelly Partners Group Holdings Limited',
    'Genusplus Group Limited','Vanguard MSCI Australian Large Companies INDEX ETF','Invictus Energy Limited','Global Value Fund Limited','Vaneck MSCI International Value ETF',
    'Big River Industries Limited','Atturra Limited','Quantum Graphite Limited','Betashares S&P/ASX Australian Technology ETF','Iodm Limited','Betashares Global Robotics and Artificial Intelligence ETF',
    'Opthea Limited','Volpara Health Technologies Limited','Vaneck MSCI Intl Small Companies Quality ETF','Wotso Property','Vaneck S&P/ASX Midcap ETF',
    'A2B Australia Limited','GENEX Power Limited','Barrow Hanley Global Share Fund (Managed Fund)','Bathurst Resources Limited','Fleetwood Limited','Paradigm Biopharmaceuticals Limited',
    'Vaneck Australian Banks ETF','Sheffield Resources Limited','Wam Strategic Value Limited','Fiducian Group Limited','Dropsuite Limited','Bailador Technology Investments Limited',
    'Southern Cross Media Group Limited','LGI Limited','Betashares Australian Dividend Harvester Fund (Managed Fund)','MACH7 Technologies Limited','FENIX Resources Limited',
    'Betashares Australian Resources Sector ETF','Anson Resources Limited','Berkeley Energia Limited','Munro Global Growth Fund (Hedge Fund)','Silk Laser Australia Limited',
    'Nexted Group Limited','Clover Corporation Limited','Droneshield Limited','Betashares Geared US Equity Fund Currency Hedged (Hedgefund)','Betashares Crude Oil INDEX ETF-Currency Hedged (Synthetic)',
    'Carnaby Resources Limited','Comet Ridge Limited','Tribune Resources Limited','PRT Company Limited','Tesserent Limited','ZETA Resources Limited','Wagners Holding Company Limited',
    'Finbar Group Limited','Highfield Resources Limited','Energy One Limited','Avjennings Limited','Lunnon Metals Limited','Redbubble Limited','Betashares Climate Change Innovation ETF',
    'Ora Banda Mining Limited','XRF Scientific Limited','Camplify Holdings Limited','Task Group Holdings Limited','EUROZ Hartleys Group Limited','Playside Studios Limited',
    'Northern Minerals Limited','Frontier Digital Ventures Limited SPONSORED','Aeris Resources Limited','Experience Co Limited','Iris Metals Limited','Vaneck MSCI International Sustainable Equity ETF',
    'Hot Chili Limited','Betashares Global Healthcare ETF - Currency Hedged','ST Barbara Limited','Aura Energy Limited','Morningstar International Shares Active ETF (Managed Fund)',
    'Austin Engineering Limited','NZME Limited','Motorcycle Holdings Limited','Aic Mines Limited','Nobleoak Life Limited','Ci Resources Limited','Xanadu Mines Limited',
    'Helios Energy Limited','Alcidion Group Limited','Reef Casino Trust','Ishares Edge MSCI World Multifactor ETF','Shaver Shop Group Limited','Danakali Limited',
    'SPDR S&P 500 ETF Trust','Peninsula Energy Limited','Waterco Limited','Vanguard International Credit Securities INDEX (Hedged) ETF','Vaneck Emerging Inc Opportunities Active ETF (Managed Fund)',
    'Ishares MSCI South Korea ETF','Vaneck MSCI Australian Sustainable Equity ETF','Alligator Energy Limited','Betashares S&P 500 Yield Maximiser Fund (Managed Fund)',
    'Electro Optic Systems Holdings Limited','Eroad Limited','Encounter Resources Limited','Russell Investments Australian Government Bond ETF','SPDR S&P/ASX 200 Resources Fund',
    'Betashares US Treasury Bond 20+YR ETF - CCY Hedged','Lithium Power International Limited','Enero Group Limited','Capral Limited','360 Capital Group','Nexgen Energy (Canada) Limited',
    'Global X Metal Securities Australia Limited','Shape Australia Corporation Limited','Silk Logistics Holdings Limited','Next Science Limited','Ishares Global High Yield Bond (Aud Hedged) ETF',
    'Oneview Healthcare Plc','Paragon Care Limited','Aurelia Metals Limited','Cash Converters International','Jervois Global Limited','Cosol Limited','Dreadnought Resources Limited',
    'Pancontinental Energy NL','Conrad Asia Energy Limited','Healthia Limited','Resource Development Group Limited','Kiland Limited','Bubs Australia Limited',
    'Maxiparts Limited','Global Data Centre Group','88 Energy Limited','Eureka Group Holdings Limited','Dacian Gold Limited','Tribeca Global Natural Resources Limited',
    'QANTM Intellectual Property Limited','Race Oncology Limited','Hastings Technology Metals Limited','DEVEX Resources Limited','Emvision Medical Devices Limited',
    'Latitude Group Holdings Limited','Bougainville Copper Limited','Ten Sixty Four Limited','Incannex Healthcare Limited','AMA Group Limited','Sunland Group Limited',
    'Gowing Bros Limited','Forager Australian Shares Fund','Red Hawk Mining Limited','Australian Vanadium Limited','5E Advanced Materials Inc','Viva Leisure Limited',
    'Murray Cod Australia Limited','Medadvisor Limited','Cti Logistics Limited','Cokal Limited','Ardea Resources Limited','Ishares S&P/ASX Small Ordinaries ETF',
    'Queensland Pacific Metals Limited','Retail Food Group Limited','Elevate Uranium Limited','Recce Pharmaceuticals Limited','Betashares Global Agriculture ETF - Currency Hedged',
    'Ansarada Group Limited','Ishares Core MSCI Australia Esg ETF','Pengana Capital Group Limited','FSA Group Limited','Betashares Martin Currie Em Fund (Managed Fund)',
    'Hillgrove Resources Limited','Rubicon Water Limited','Ishares Core Corporate Bond ETF','Cobalt Blue Holdings Limited','Saunders International Limited',
    'Hipages Group Holdings Limited','Smart Parking Limited','Peak Rare EARTHS Limited','EQ Resources Limited','Talon Energy Limited','Betashares U.S. Dollar ETF',
    'Archer Materials Limited','REX Minerals Limited','Lark Distilling Co. Limited','SPDR S&P/ASX 200 Financials Ex A-REIT Fund','Clime Capital Limited',
    'Newfield Resources Limited','Regional Express Holdings Limited','Magellan Global Equities Fund Currency Hedged (Managed Fund)','City Chic Collective Limited',
    'Global X Semiconductor ETF','Essential Metals Limited','Spheria Emerging Companies Limited','Orion Minerals Limited','Vaneck China New Economy ETF','Ariadne Australia Limited',
    'CD Private Equity Fund Iii','Empire Energy Group Limited','Vaneck Global Clean Energy ETF','Panoramic Resources Limited','Group 6 Metals Limited','Legend Mining Limited',
    'Janison Education Group Limited','Green Technology Metals Limited','Global X Copper Miners ETF','Catalyst Metals Limited','Altech Batteries Limited SPONSORED',
    'Magnis Energy Technologies Limited','Intelligent Investor Aus Equity Growth Fund (Managed Fund)','Energy World Corporation Limited','Embark Early Education Limited',
    'Coventry Group Limited','Engenco Limited','Fidelity Global Demographics Fund (Managed Fund)','Microba Life Sciences Limited','Minerals 260 Limited',
    'Proteomics International Laboratories Limited','E&P Financial Group Limited','American West Metals Limited','Mindax Limited','Shine Justice Limited',
    'Betmakers Technology Group Limited','PPK Group Limited','Calidus Resources Limited','Black Rock Mining Limited','European Metals Holdings Limited','Image Resources NL',
    'Platinum Asia Fund (Quoted Managed Hedge Fund)','Legacy Iron Ore Limited','Australian Vintage Limited','Step One Clothing Limited','SDI Limited',
    'Acusensus Limited','Ikegps Group Limited','Santana Minerals Limited','Jindalee Resources Limited','Globe International Limited','Imricor Medical Systems Inc',
    'Envirosuite Limited','Brisbane Broncos Limited','Beacon Minerals Limited','European Lithium Limited','Fluence Corporation Limited','New Zealand King Salmon Investments Limited',
    'DOTZ Nano Limited','Firstwave Cloud Technology Limited','Laserbond Limited','Korvest Limited','Structural Monitoring Systems Plc','Naos Small Cap Opportunities Company Limited',
    'Sezzle Inc','Ashley Services Group Limited','Synertec Corporation Limited','Freelancer Limited','The Market Herald Limited','Bisalloy Steel Group Limited',
    'Theta Gold Mines Limited','Byron Energy Limited','HAZER Group Limited','Caravel Minerals Limited','HEJAZ Equities Fund (Managed Fund)','Thorney Opportunities Limited',
    'Metro Mining Limited','Adore Beauty Group Limited','Otto Energy Limited','Andromeda Metals Limited','Shriro Holdings Limited','Frontier Energy Limited',
    'Global X Euro STOXX 50 ETF','Kinetiko Energy Limited','Sandon Capital Investments Limited','Tivan Limited','Challenger Gold Limited','Sunrise Energy Metals Limited',
    'Element 25 Limited','Global X Ultra Short Nasdaq 100 Hedge Fund','360 Capital REIT','Keypath Education International Inc','Hitech Group Australia Limited',
    'Veem Limited','Airtasker Limited','Environmental Group Limited (the)','Minbos Resources Limited','Betashares India Quality ETF','Credit Clear Limited',
    'MLG OZ Limited','Ishares Global Aggregate Bond Esg (Aud Hedged) ETF','Rumble Resources Limited','Latrobe Magnesium Limited','Namoi Cotton Limited',
    'Diatreme Resources Limited','GTN Limited','RHYTHM Biosciences Limited','Sierra Rutile Holdings Limited','National Tyre & Wheel Limited','Excelsior Capital Limited',
    'Curvebeam Ai Limited','Lepidico Limited','New Zealand Oil & Gas Limited','Acorn Capital Investment Fund Limited','Ryder Capital Limited','Galileo Mining Limited',
    'Betashares Japan ETF-Currency Hedged','Havilah Resources Limited','Vita Life Sciences Limited','Move Logistics Group Limited','Poseidon Nickel Limited',
    'Amaero International Limited','Genmin Limited','Vanguard Ethically Conscious GLB Agg Bond INDEX (Hedged) ETF','Clean Seas Seafood Limited','Ausgold Limited',
    'Cyprium Metals Limited','Orthocell Limited','Medical Developments International Limited','Betashares CRYPTO Innovators ETF','Rand Mining Limited',
    'Mitchell Services Limited','Vysarn Limited','Troy Resources Limited','Pacific Edge Limited','Tigers Realm Coal Limited','FBR Limited','Intelligent Investor Aus Equity Income Fund (Managed Fund)',
    'Astron Corporation Limited','Vaneck Morningstar Australian Moat Income ETF','New World Resources Limited','VHM Limited','Galena Mining Limited','Iron Road Limited',
    'DRA Global Limited','Thorney Technologies Limited','Rectifier Technologies Limited','Joyce Corporation Limited','Tamawood Limited','Wiluna Mining Corporation Limited',
    'Echoiq Limited','Zeotech Limited','Walkabout Resources Limited','Sequoia Financial Group Limited','Clearvue Technologies Limited','Cannindah Resources Limited',
    'Betashares Aust Small Companies Select Fund (Managed Fund)','Adrad Holdings Limited','Microequities Asset Management Group Limited','ROX Resources Limited','Sietel Limited',
    'Montaka GBL Long Only Equities Fund (Managed Fund)','Intelligent Investor Ethical Share Fund (Managed Fund)','Hancock & Gore Limited','KGL Resources Limited',
    'Sunstone Metals Limited','Vaneck Video Gaming and Esports ETF','TMK Energy Limited','Bluglass Limited','S2 Resources Limited','Count Limited','Auteco Minerals Limited',
    'Global X S&P 500 High Yield Low Volatility ETF',"Mcpherson's Limited",'Advance Zinctek Limited','A-Cap Energy Limited','Chesser Resources Limited','Pointerra Limited',
    'Critical Resources Limited','Besra Gold Inc','Anteotech Limited','Vaneck Global Healthcare Leaders ETF','Ionic Rare EARTHS Limited','Mayfield Childcare Limited',
    'Genetic Signatures Limited','Titan Minerals Limited','Betashares Global Shares ETF','Switzer Dividend Growth Fund (Managed Fund)','Tyranna Resources Limited',
    'Strickland Metals Limited','Global X S&P/ASX 200 High Dividend ETF','Kairos Minerals Limited','Plenti Group Limited','Dusk Group Limited','Dome Gold Mines Limited',
    'Technology Metals Australia Limited','Apiam Animal Health Limited','Investigator Resources Limited','Hartshead Resources NL','Reckon Limited','Micro-X Limited',
    'VRX Silica Limited','Inoviq Limited','Integrated Research Limited','Swoop Holdings Limited','Pental Limited','Somnomed Limited','Betashares Ethical Diversified High Growth ETF',
    'Optiscan Imaging Limited','Ai-Media Technologies Limited','Superior Resources Limited','Global X Ultra Long Nasdaq 100 Hedge Fund','Prescient Therapeutics Limited',
    'Blackstone Minerals Limited','Elixir Energy Limited','Pure Hydrogen Corporation Limited','Ecograf Limited','Peel Mining Limited','Ixup Limited','Lion Selection Group Limited',
    'Tungsten Mining NL','American Rare EARTHS Limited','Asf Group Limited','Brookside Energy Limited','Black Cat Syndicate Limited','MC Mining Limited',
    'Vmoto Limited','Simonds Group Limited','Ecofibre Limited','Lithium Energy Limited','Nova Minerals Limited','Mayur Resources Limited','Neurizer Limited','Mcgrath Limited',
    'Good Drinks Australia Limited','Duxton Farms Limited','Alphinity Global Sustainable Fund (Managed Fund)','CD Private Equity Fund Ii','Po Valley Energy Limited','Canyon Resources Limited',
    'Lakes Blue Energy NL','Nuenergy Gas Limited','Antisense Therapeutics Limited','Agrimin Limited','Global X India Nifty 50 ETF','Lucapa Diamond Company Limited',
    'Orcoda Limited','Schroder Real Return (Managed Fund)','Starpharma Holdings Limited','Focus Minerals Limited','Alliance Nickel Limited','Energy Transition Minerals Limited',
    'Salter Brothers Emerging Companies Limited','TPC Consolidated Limited','Earlypay Limited','Widgie Nickel Limited','Touch Ventures Limited','Pro-Pac Packaging Limited',
    'Betashares MRTN Currie RL Inc Fund (Managed Fund)','Aston Minerals Limited','Beamtree Holdings Limited','Wam Active Limited','Betashares Global Gold Miners ETF - Currency Hedged',
    'Vaneck MSCI Multifactor Em Markets Equity ETF','Aims Property Securities Fund','Moneyme Limited','Meeka Metals Limited','Buru Energy Limited','Wa Kaolin Limited',
    'Ishares Edge MSCI Australia Multifactor ETF','Matrix Composites & Engineering Limited','Ishares Ftse GBL Infrastructure (Aud Hedged) ETF','Calima Energy Limited',
    'Thorn Group Limited','Donaco International Limited','Arizona Lithium Limited','Arovella Therapeutics Limited','Prospa Group Limited','Ellerston Asia Growth Fund (Hedge Fund)',
    'Betashares Cloud Computing ETF','Austral Resources Australia Limited','Midway Limited','Cann Group Limited','Intelligent Monitoring Group Limited','Vital Metals Limited','Morphic Ethical Equities Fund Limited',
    'Noble Helium Limited','Auctus Investment Group Limited','Kingsrose Mining Limited','Ironbark Capital Limited','Loyal Lithium Limited','CYGNUS Metals Limited',
    'Little Green Pharma Limited','Scidev Limited','Eumundi Group Limited','True North Copper Limited','Betashares Managed Risk Global Share Fund (Managed Fund)','Centrepoint Alliance Limited',
    'Boom Logistics Limited','Gale Pacific Limited','Naos Emerging Opportunities Company Limited','Universal Biosensors Inc','Kalium Lakes Limited',
    'Betashares Australian Equities Bear (Hedge Fund)','Future Battery Minerals Limited','US Student Housing REIT','Astral Resources NL','Vaneck Small Companies Masters ETF',
    'Icandy Interactive Limited','Hammer Metals Limited','Tombador Iron Limited','Ishares J.P. Morgan Usd Emerging Markets (Aud Hedged) ETF','Austco Healthcare Limited','Maggie Beer Holdings Limited',
    'Raiden Resources Limited','Global X Hydrogen ETF','Russell Investments Australian Semi-Government Bond ETF','Lumos Diagnostics Holdings Limited','Aspire Mining Limited',
    'Terramin Australia Limited','Euro Manganese Inc','AVA Risk Group Limited','Province Resources Limited','Sports Entertainment Group Limited','Prime Financial Group Limited',
    'Bluebet Holdings Limited','Avada Group Limited','Toro Energy Limited','Renergen Limited','Teaminvest Private Group Limited','BNK Banking Corporation Limited',
    'Centrex Limited','Southern Cross Gold Limited','Advanced Health Intelligence Limited','Antipa Minerals Limited','RAIZ Invest Limited','Wide Open Agriculture Limited',
    'Wisr Limited SPONSORED','KIN Mining NL','Artemis Resources Limited','Actinogen Medical Limited','Openpay Group Limited','CUE Energy Resources Limited',
    'Eildon Capital Group','Betashares Global Quality Leaders ETF Currency Hedged','Lithium Australia Limited','Australian Pacific Coal Limited','Elsight Limited',
    'Vection Technologies Limited','First Graphene Limited','Prospect Resources Limited','Betashares Europe ETF-Currency Hedged','Tanami Gold NL','Flagship Investments Limited',
    'BENZ Mining Corp','SPDR MSCI World Quality MIX Fund','Alternative Investment Trust','Nico Resources Limited','Neurotech International Limited',
    'FFI Holdings Limited','Betashares Global Banks ETF - Currency Hedged','Far East Gold Limited','Harmoney Corp Limited','Top Shelf International Holdings Limited',
    'Lowell Resources Fund','Betashares Global Uranium ETF','Straker Limited','Prophecy International Holdings Limited','Whispir Limited','Zenith Minerals Limited',
    'RTG Mining Inc','Metarock Group Limited','Betashares Australian Financials Sector ETF','Barton Gold Holdings Limited','Loomis Sayles GBL EQ Fund (Quoted Managed Fund)',
    'SPDR S&P/ASX 200 Esg Fund','Perennial Better Future Fund (Managed Fund)','Polymetals Resources Limited','Magontec Limited','BSA Limited','Triton Minerals Limited',
    'Horizon Gold Limited','Pan Asia Metals Limited','Blue Star Helium Limited','Strategic Elements Limited','Dubber Corporation Limited','Veris Limited',
    'Novatti Group Limited','Redflow Limited','Kinatico Limited','Metalstech Limited SPONSORED','Adacel Technologies Limited','Noumi Limited','Central Petroleum Limited',
    'Dynamic Group Holdings Limited','BWX Limited','Naos Ex-50 Opportunities Company Limited','Argenica Therapeutics Limited','Kingston Resources Limited',
    'Infinity Lithium Corporation Limited','Desane Group Holdings Limited','Cirrus Networks Holdings Limited','Sovereign Cloud Holdings Limited','Pacific Nickel Mines Limited SPONSORED',
    'Li-S Energy Limited','Painchek Limited','Impact Minerals Limited SPONSORED','Invion Limited','Hawthorn Resources Limited','Mayfield Group Holdings Limited',
    'Change Financial Limited','Mustera Property Group Limited','De.Mem Limited','FAR Limited','Reach Resources Limited','Webcentral Limited','Red River Resources Limited',
    'Income Asset Management Group Limited','Global X S&P Biotech ETF','Selfwealth Limited','Vanadium Resources Limited','State GAS Limited','Etherstack Plc','Ora Gold Limited',
    'Katana Capital Limited','Ras Technology Holdings Limited','Nova EYE Medical Limited','Carbon Revolution Limited','Blackwall Limited','REY Resources Limited',
    'SPDR S&P/ASX Australian Bond Fund','Australian Rare EARTHS Limited','Betashares Ethical Diversified Growth ETF','Vintage Energy Limited','KAZIA Therapeutics Limited',
    'Duketon Mining Limited','Morella Corporation Limited','CZR Resources Limited','Macarthur Minerals Limited','Emmerson Resources Limited','Volt Resources Limited',
    'Compumedics Limited','Vaneck Morningstar International Wide Moat ETF','Xref Limited','Great Boulder Resources Limited','Warriedar Resources Limited','Montaka Global Extension Fund (Quoted Managed Hedge Fund)',
    'Jade Gas Holdings Limited','Firebrick Pharma Limited','Rma Global Limited','Xtek Limited','Aerometrex Limited','Alto Metals Limited','West Wits Mining Limited',
    'Clime Capital Limited','Sensen Networks Limited','Pioneer Credit Limited','Provaris Energy Limited','Nuheara Limited','Kip Mcgrath Education Centres Limited',
    'Greenvale Energy Limited','Richmond Vanadium Technology Limited','Pureprofile Limited','Mineral Commodities Limited','Pilot Energy Limited','Lefroy Exploration Limited',
    'Diverger Limited','Urbanise.com Limited','Kuniko Limited','Marley Spoon Se','Tombola Gold Limited','Mad Paws Holdings Limited','Foresta Group Holdings Limited',
    'ST George Mining Limited','92 Energy Limited','Einvest Income Generator Fund (Managed Fund)','Marmota Limited','Retech Technology Co. Limited','ADX Energy Limited',
    'Soco Corporation Limited','Aerison Group Limited','Vaneck Bentham GL Cap Se Active ETF (Managed Fund)','Indiana Resources Limited','Trek Metals Limited','Falcon Metals Limited',
    'Omega Oil & Gas Limited','Academies Australasia Group Limited','QEM Limited','Netlinkz Limited','Tlou Energy Limited','Cryosite Limited','Blue Energy Limited','Global Masters Fund Limited',
    'Boab Metals Limited','Munro Climate Change Leaders Fund (Managed Fund)','DGR Global Limited','WIA Gold Limited','Mosaic Brands Limited','SPDR S&P/ASX Australian Government Bond Fund',
    'Butn Limited','Unico Silver Limited','Pharmaxis Limited','Bass Oil Limited','GWR Group Limited','WRKR Limited','Eagle Mountain Mining Limited','Hawsons Iron Limited','Triangle Energy (Global) Limited',
    'Secos Group Limited','Respiri Limited','Evolution Energy Minerals Limited','Archtis Limited','Field Solutions Holdings Limited','Stavely Minerals Limited','Pursuit Minerals Limited',
    'News Corporation','Aspermont Limited','Pentanet Limited','Adveritas Limited','Parkway Corporate Limited','Clime Investment Management Limited','WT Financial Group Limited',
    'Strata Investment Holdings Plc','Western Mines Group Limited','Spirit Technology Solutions Limited','Manuka Resources Limited','Turaco Gold Limited','Comms Group Limited',
    'Horizon Minerals Limited','Navarre Minerals Limited','Magnetite Mines Limited','Eclipse Metals Limited','Damstra Holdings Limited','Digitalx Limited',
    'CD Private Equity Fund I','Ecargo Holdings Limited','Red Metal Limited','Cadence Opportunities Fund Limited','Senetas Corporation Limited','Alloggio Group Limited',
    'Altamin Limited','Industrial Minerals Limited','Betashares Global Income Leaders ETF','Greenwing Resources Limited','NGE Capital Limited','Jatcorp Limited',
    'Dimerix Limited','Betashares Managed Risk AUS SH Fund (Managed Fund)','Alara Resources Limited','Resource Mining Corporation Limited','Elementos Limited',
    'Energy Metals Limited','Pharmaust Limited','Vaneck 1-3 Month US Treasury Bond ETF','Solis Minerals Limited','SPDR S&P/ASX Small Ordinaries Fund','Carnavale Resources Limited',
    'Bioxyne Limited','Kaiser Reef Limited','Carawine Resources Limited','Red Sky Energy Limited','Australis Oil & Gas Limited','Daintree HYBRID Opportunities Fund (Managed Fund)',
    'Manhattan Corporation Limited','Talisman Mining Limited','Ioupay Limited','Harvest Technology Group Limited','Coda Minerals Limited','Corum Group Limited',
    'LCL Resources Limited','Intell Invest Select Value SHR Fund (Managed Fund)','Imexhs Limited','Biotron Limited','Atomos Limited','Decmil Group Limited',
    'EZZ Life Science Holdings Limited','RAREX Limited','Birddog Technology Limited','Saturn Metals Limited','Spenda Limited','Buxton Resources Limited','The Original Juice Co. Limited',
    'Glennon Small Companies Limited','Venture Minerals Limited','Resonance Health Limited','FYI Resources Limited','Cluey Limited','Amani Gold Limited','Talius Group Limited',
    'QX Resources Limited','H&G High Conviction Limited','Metro Performance Glass Limited','Metallica Minerals Limited','Decmil Group Limited','Battery Age Minerals Limited SPONSORED',
    'EDU Holdings Limited','Surefire Resources NL','Celsius Resources Limited','Emyria Limited','Hannans Limited','South HARZ Potash Limited','Jayride Group Limited',
    'Sihayo Gold Limited','Verbrec Limited','ECS Botanics Holdings Limited','Belararox Limited','Whitefield Industrials Limited','Seafarms Group Limited','Advanced Share Registry Limited',
    'RPM Automotive Group Limited',
    'ANAX Metals Limited',
    'Wellard Limited',
    'Alicanto Minerals Limited',
    'Ensurance Limited',
    'Tian An Australia Limited',
    'Venus Metals Corporation Limited',
    'Fat Prophets Global Contrarian Fund Limited',
    'Nexus Minerals Limited',
    'Unith Limited',
    'Medallion Metals Limited',
    'Cynata Therapeutics Limited',
    'Weststar Industrial Limited',
    'Splitit Payments Limited',
    'Fertoz Limited',
    'Jaxsta Limited',
    'Cleanspace Holdings Limited',
    'Metals Australia Limited',
    'Genetic Technologies Limited',
    'Galilee Energy Limited',
    'Transmetro Corporation Limited',
    'Wellnex Life Limited',
    'Living Cell Technologies Limited',
    'IDT Australia Limited',
    'Booktopia Group Limited',
    'Betashares MRTN Currie EQY Inc Fund (Managed Fund)',
    'Mandrake Resources Limited',
    'Radiopharm Theranostics Limited',
    'Suvo Strategic Minerals Limited',
    'Betashares Energy Transition Metals ETF',
    'Embelton Limited',
    'Adherium Limited',
    'Jupiter Energy Limited',
    'ABX Group Limited',
    'Tennant Minerals Limited',
    'AML3D Limited',
    'Greentech Metals Limited',
    'Connexion Telematics Limited',
    'Oncosil Medical Limited',
    'Magnum Mining and Exploration Limited',
    'Equatorial Resources Limited',
    'Heramed Limited',
    '360 Capital Mortgage REIT',
    'Betashares Ethical Diversified Balanced ETF',
    'Ishares Yield Plus ETF',
    'Rhinomed Limited',
    'Clean TEQ Water Limited',
    'Bcal Diagnostics Limited',
    'Vectus Biosystems Limited',
    'Biome Australia Limited',
    'Recharge Metals Limited',
    'Buddy Technologies Limited',
    'Tesoro Gold Limited',
    'Cardiex Limited',
    'ARTRYA Limited',
    'Brightstar Resources Limited',
    'Copper Strike Limited',
    'Naos Emerging Opportunities Company Limited',
    'Australian Silica Quartz Group Limited',
    'A1 Investments & Resources Limited',
    'Beam Communications Holdings Limited',
    'Melodiol Global Health Limited',
    'Ambertech Limited',
    'Activeport Group Limited',
    'Jameson Resources Limited',
    'Itech Minerals Limited',
    'Nagambie Resources Limited',
    'Globe Metals & Mining Limited',
    'Quickstep Holdings Limited',
    'Xreality Group Limited',
    'Chimeric Therapeutics Limited',
    'Imagion Biosystems Limited',
    'Alterity Therapeutics Limited',
    'Shekel Brainweigh Limited',
    'Cobre Limited',
    'Phosco Limited',
    'Okapi Resources Limited',
    'Vaneck Ftse China A50 ETF',
    'Scorpion Minerals Limited',
    'Gold Mountain Limited',
    'Carbonxt Group Limited',
    'SPDR S&P Emerging Markets Carbon Control Fund',
    'Cosmos Exploration Limited',
    'SKY Metals Limited',
    'Kleos Space S.A',
    'Future Metals NL',
    'ECP Emerging Growth Limited',
    'Flagship Investments Limited',
    'Findi Limited',
    'Apollo Minerals Limited',
    'Livehire Limited',
    'Parabellum Resources Limited',
    'Sarytogan Graphite Limited',
    'Sparc Technologies Limited',
    'Atlas Pearls Limited',
    'Betashares Australian Quality ETF',
    'Complii Fintech Solutions Limited',
    'Magmatic Resources Limited',
    'Aeon Metals Limited',
    'PATRYS Limited',
    'SKYFII Limited',
    'BBX Minerals Limited',
    'Ishares Edge MSCI Australia Minimum Volatility ETF',
    'Investsmart Group Limited',
    'Peppermint Innovation Limited',
    'Lithium Universe Limited SPONSORED',
    'Frugl Group Limited',
    'Yojee Limited',
    'Midas Minerals Limited',
    'K2 Asset Management Holdings Limited',
    'Platina Resources Limited',
    'Maronan Metals Limited',
    'Immuron Limited',
    'Everest Metals Corporation Limited',
    'Yellow Brick Road Holdings Limited',
    'Power Minerals Limited',
    'Iceni Gold Limited',
    'Monash Investors SML Companies Trust (Hedge Fund)',
    'Qmines Limited',
    'ENTYR Limited',
    'Titomic Limited',
    'Axiom Properties Limited',
    'Victor Group Holdings Limited',
    'Kalamazoo Resources Limited',
    'Auscann Group Holdings Limited',
    'Odyssey Gold Limited',
    'Doctor Care Anywhere Group Plc',
    'Xantippe Resources Limited',
    'White Rock Minerals Limited',
    'Tambourah Metals Limited',
    'Matador Mining Limited',
    'Askari Metals Limited',
    'Avenira Limited',
    'Farm Pride Foods Limited',
    'Atomo Diagnostics Limited',
    'Golden Rim Resources Limited',
    'Akora Resources Limited',
    'Environmental Clean Technologies Limited',
    'Amplia Therapeutics Limited',
    '8COMMON Limited',
    'Cazaly Resources Limited',
    'Millennium Services Group Limited',
    'Caspin Resources Limited',
    'Aldoro Resources Limited',
    'Lanthanein Resources Limited',
    'BPH Energy Limited',
    'Victory Metals Limited',
    'Pacgold Limited',
    'Orbital Corporation Limited',
    'SKS Technologies Group Limited',
    'Naos Ex-50 Opportunities Company Limited',
    'Cassius Mining Limited',
    'Orion Metals Limited',
    'Sabre Resources Limited',
    'EVZ Limited',
    'Peregrine Gold Limited',
    'Viridis Mining and Minerals Limited',
    'Lithium Plus Minerals Limited',
    'Sunshine Metals Limited',
    'Bulletin Resources Limited',
    'PNX Metals Limited',
    'Ardiden Limited',
    'Vanguard Global Minimum Volatility Active ETF (Managed Fund)',
    'NSX Limited',
    'Nuchev Limited',
    'Beston Global Food Company Limited',
    'K2FLY Limited',
    'Bio-Gene Technology Limited',
    'Antilles Gold Limited',
    'Grand Gulf Energy Limited',
    'Vaneck Gold Bullion ETF',
    'Strike Resources Limited',
    'Astute Metals NL',
    'N1 Holdings Limited',
    'OAR Resources Limited',
    'Apostle Dundas Global Equity Classd (Managed Fund)',
    'Fitzroy River Corporation Limited',
    'Carnegie Clean Energy Limited',
    'Phoslock Environmental Technologies Limited',
    'Lion One Metals Limited',
    'Geopacific Resources Limited',
    'Gti Energy Limited',
    'Beforepay Group Limited',
    'International Graphite Limited',
    'Mount Ridley Mines Limited',
    'King River Resources Limited',
    'London City Equities Limited',
    'Althea Group Holdings Limited',
    'Fat Prophets Global Property Fund',
    'Valor Resources Limited',
    'Flexiroam Limited',
    'Minrex Resources Limited',
    'Kalina Power Limited',
    'Avecho Biotechnology Limited',
    'AJ Lucas Group Limited',
    'Almonty Industries Inc',
    'Gold Hydrogen Limited',
    'Medlab Clinical Limited',
    'East 33 Limited',
    'Dateline Resources Limited SPONSORED',
    'Odin Metals Limited',
    'EV Resources Limited',
    'NGX Limited',
    'Sportshero Limited',
    'Af Legal Group Limited',
    'Cleo Diagnostics Limited',
    'Voltaic Strategic Resources Limited',
    'Acumentis Group Limited',
    'Revasum Inc',
    'Advanced Braking Technology Limited',
    'Greenstone Resources Limited',
    'Rimfire Pacific Mining Limited',
    'Vaneck Global Listed Private Equity ETF',
    'Burley Minerals Limited',
    'Podium Minerals Limited',
    'High Peak Royalties Limited',
    'Asian American Medical Group Limited',
    'Jpmorgan EQ Prem Income Active ETF (Managed Fund)',
    'Castile Resources Limited',
    'Augustus Minerals Limited',
    'Norwood Systems Limited',
    'Quickfee Limited',
    'Aquirian Limited',
    'Baumart Holdings Limited',
    'FELIX Group Holdings Limited',
    'Corella Resources Limited',
    'Lode Resources Limited',
    'Riedel Resources Limited',
    'Mont Royal Resources Limited',
    'Finexia Financial Group Limited',
    'Citigold Corporation Limited',
    '3D Oil Limited',
    'Great Southern Mining Limited',
    'Paterson Resources Limited',
    'INVEX Therapeutics Limited',
    'Bluechiip Limited',
    'Savannah Goldfields Limited',
    'Evergreen Lithium Limited',
    'Energy Technologies Limited',
    'Fatfish Group Limited',
    'Alchemy Resources Limited',
    'Hamelin Gold Limited',
    'Revolver Resources Holdings Limited',
    'Incentiapay Limited',
    'ACRUX Limited',
    'Oceana Lithium Limited SPONSORED',
    'Papyrus Australia Limited',
    'Renu Energy Limited',
    'Resource Base Limited',
    'Betashares Electric Vehicles and FTR Mobility ETF',
    'Matsa Resources Limited',
    'Metal Bank Limited',
    'Austral Gold Limited',
    'Polarx Limited',
    'Memphasys Limited',
    'Charger Metals NL',
    'The Agency Group Australia Limited',
    'Toubani Resources Inc',
    'Mobilicom Limited',
    'Mako Gold Limited',
    'BIR Financial Limited',
    'Rewardle Holdings Limited',
    'Adslot Limited',
    'Allegiance Coal Limited',
    'Petratherm Limited',
    'Neuroscientific Biopharmaceuticals Limited',
    'Lodestar Minerals Limited',
    'Argent Minerals Limited',
    'Stealth Global Holdings Limited',
    'Cufe Limited',
    'Cardno Limited',
    'Armour Energy Limited',
    'Perpetual Resources Limited',
    'Star Combo Pharma Limited',
    'Halo Technologies Holdings Limited',
    '1ST Group Limited',
    'Gold 50 Limited',
    'Copper Search Limited',
    'Global X Metal Securities Australia Limited',
    'Alvo Minerals Limited',
    'Tissue Repair Limited',
    'Pure Foods Tasmania Limited',
    'Ishares Ftse GBL Property Ex Aus (Aud Hedged) ETF',
    'Nordic Nickel Limited',
    'Solstice Minerals Limited',
    'Torque Metals Limited',
    'Southern Palladium Limited',
    'Zelira Therapeutics Limited',
    'Jcurve Solutions Limited',
    'Siren Gold Limited',
    'EQUUS Mining Limited',
    'Platinum Transition (Quoted Managed Hedge Fund)',
    'Betashares Strong Australian Dollar Fund (Hedge Fund)',
    'Mosaic Brands Limited',
    'Stelar Metals Limited',
    'GBM Resources Limited',
    'Hills Limited',
    'Credit Intelligence Limited',
    'Leeuwin Metals Limited',
    'Ballymore Resources Limited',
    'Firetail Resources Limited',
    'Eden Innovations Limited',
    'Patriot Lithium Limited',
    'RLF Agtech Limited',
    'Hudson Investment Group Limited',
    'Lachlan Star Limited',
    'Estrella Resources Limited',
    'Castle Minerals Limited',
    'Tasfoods Limited',
    'HEJAZ Property Fund (Managed Fund)',
    'Livetiles Limited',
    'Evion Group NL',
    'Ironbark ZINC Limited',
    'Rare Foods Australia Limited',
    'Megado Minerals Limited',
    'Metgasco Limited',
    'MGC Pharmaceuticals Limited',
    'Xamble Group Limited',
    'AXP Energy Limited',
    'HELIX Resources Limited',
    'Asra Minerals Limited',
    'Woomera Mining Limited',
    'Riversgold Limited',
    'Hubify Limited',
    'BOD Science Limited',
    'ZICOM Group Limited',
    'Kingfisher Mining Limited',
    'Many Peaks Gold Limited',
    'Eastern Resources Limited',
    'Openn Negotiation Limited',
    'Vaughan Nelson Global Smid Fund (Managed Fund)',
    'Australian Dairy Nutritionals Limited',
    'Hygrovest Limited',
    'Equity Trustees Limited',
    'OD6 Metals Limited',
    'Alma Metals Limited',
    'Associate Global Partners Limited',
    'Krakatoa Resources Limited',
    'Hyterra Limited',
    'SI6 Metals Limited',
    'Stonehorse Energy Limited',
    'Gratifii Limited',
    'Sensore Limited',
    'Design Milk Co Limited',
    'Infinity Mining Limited',
    'Firetrail S3 Global Opps Fund (Managed Fund)',
    'Osteopore Limited',
    'Aurora Energy Metals Limited',
    'Gullewa Limited',
    'Volt Power Group Limited',
    'Reward Minerals Limited',
    'Great Western Exploration Limited',
    'Marquee Resources Limited',
    'Golden Mile Resources Limited',
    'Noxopharm Limited',
    'Prodigy Gold NL',
    'Land & Homes Group Limited',
    'VONEX Limited',
    'Tinybeans Group Limited',
    'Whitehawk Limited',
    'Australian Mines Limited',
    'Nimy Resources Limited',
    'One Click Group Limited',
    'Ragnar Metals Limited',
    'Fintech Chain Limited',
    'Balkan Mining and Minerals Limited',
    'Koba Resources Limited',
    'Rent.com.Au Limited',
    'Cyclone Metals Limited',
    'Mighty Craft Limited',
    'Yari Minerals Limited',
    'Red Mountain Mining Limited',
    'Norwest Minerals Limited',
    'Stellar Resources Limited',
    'White Cliff Minerals Limited',
    'Arcadia Minerals Limited',
    'Southern Hemisphere Mining Limited',
    'GLG Corp Limited',
    'Auking Mining Limited',
    'Truscreen Group Limited',
    'ECP Emerging Growth Limited',
    'Betashares British Pound ETF',
    'Enegex Limited',
    'Uscom Limited',
    'Ausquest Limited',
    'Lion Energy Limited',
    'Babylon Pump & Power Limited',
    'Ep&T Global Limited',
    'Pivotal Metals Limited',
    'Alexium International Group Limited',
    'Larvotto Resources Limited',
    'Keybridge Capital Limited',
    'Intra Energy Corporation Limited',
    'Kingsland Global Limited',
    'Olympio Metals Limited',
    'Adalta Limited',
    'Errawarra Resources Limited',
    'Adavale Resources Limited',
    'Classic Minerals Limited',
    'Bounty Oil & Gas NL',
    'Mitre Mining Corporation Limited',
    'Bikeexchange Limited',
    'Betashares Strong U.S. Dollar Fund (Hedge Fund)',
    'Marvel Gold Limited',
    'Firebird Metals Limited',
    'Juno Minerals Limited',
    'Cape Range Limited',
    'Yandal Resources Limited',
    'Javelin Minerals Limited',
    'Metal Hawk Limited',
    'Conico Limited',
    'Aoris Int Fund (Class D) (Hedged) (Managed Fund)',
    'Global Masters Fund Limited',
    'Austchina Holdings Limited',
    'Lycaon Resources Limited',
    'Gateway Mining Limited',
    'Taiton Resources Limited',
    'Newpeak Metals Limited',
    'Viking Mines Limited',
    'Inca Minerals Limited',
    'Medibio Limited',
    'Site Group International Limited',
    'Streamplay Studio Limited',
    'Castillo Copper Limited',
    'Traffic Technologies Limited',
    'Nanoveu Limited',
    'Arrow Minerals Limited',
    '1414 Degrees Limited',
    'RUBIX Resources Limited',
    'Ark Mines Limited',
    'CPT Global Limited',
    'Swift Networks Group Limited',
    'SIV Capital Limited',
    'Resources & Energy Group Limited',
    'Maximus Resources Limited',
    'ZOOM2U Technologies Limited',
    'Green Critical Minerals Limited',
    'FELIX Gold Limited',
    'FLYNN Gold Limited',
    'Equity Trustees Limited',
    'Equity Trustees Limited',
    'Xpon Technologies Group Limited',
    'Domacom Limited',
    'Roolife Group Limited',
    'Knosys Limited',
    'Nanollose Limited',
    'Motio Limited',
    'Corazon Mining Limited',
    'CAQ Holdings Limited',
    'Thrive Tribe Technologies Limited',
    'Renegade Exploration Limited',
    'Broo Limited',
    'Athena Resources Limited',
    'Titanium Sands Limited',
    'Equity Trustees Limited',
    'Inhalerx Limited',
    'Lincoln Minerals Limited',
    'DTI Group Limited',
    'Australian Critical Minerals Limited',
    'Linius Technologies Limited',
    'Innlanz Limited',
    'K2 Australian Small Cap Fund (Hedge Fund)',
    'New Talisman Gold Mines Limited',
    'Wiseway Group Limited',
    'GCX Metals Limited',
    'Australasian Metals Limited',
    'Black Canyon Limited',
    'Gladiator Resources Limited',
    'Live Verdure Limited',
    'Aguia Resources Limited',
    'Equity Trustees Limited',
    '8I Holdings Limited',
    'Schrole Group Limited',
    'Moab Minerals Limited',
    'BLAZE Minerals Limited',
    'ZOONO Group Limited',
    'Way 2 Vat Limited',
    'Iltani Resources Limited',
    'Global Health Limited',
    'Spacetalk Limited',
    'FOS Capital Limited',
    'Kore Potash Plc',
    'X2M Connect Limited',
    'Locality Planning Energy Holdings Limited',
    'Oldfields Holdings Limited',
    'Icetana Limited',
    'Accelerate Resources Limited',
    'African Gold Limited',
    'Critical Minerals Group Limited',
    'HYDRIX Limited',
    'PVW Resources Limited',
    'Dynamic Metals Limited',
    'SRJ Technologies Group Plc',
    'Admiralty Resources NL',
    'Truscott Mining Corporation Limited',
    'Southern Gold Limited',
    'Horseshoe Metals Limited',
    'Freehill Mining Limited',
    'Ragusa Minerals Limited',
    'Cradle Resources Limited',
    'Control Bionics Limited',
    'Battery Minerals Limited',
    'Aruma Resources Limited',
    'Emetals Limited',
    'Great Divide Mining Limited',
    'Audalia Resources Limited',
    'Kingsland Minerals Limited',
    'Betashares Interest Rate Hedged Aus Corp Bond ETF',
    'Odessa Minerals Limited',
    'Chilwa Minerals Limited',
    'Legacy Minerals Holdings Limited',
    'Metalicity Limited',
    'Western Yilgarn NL',
    'Coppermoly Limited',
    'Native Mineral Resources Holdings Limited',
    "Toys'R'US ANZ Limited",
    'Korab Resources Limited',
    'Whitebark Energy Limited',
    'Argonaut Resources NL',
    'Pure Resources Limited',
    'Readcloud Limited',
    'R3D Resources Limited',
    'Ookami Limited',
    'Golden Deeps Limited',
    'Terra Uranium Limited',
    'ARC Funds Limited',
    'The Hydration Pharmaceuticals Company Limited',
    'North Stawell Minerals Limited',
    'New Age Exploration Limited',
    'Todd River Resources Limited',
    'Ignite Limited',
    'Aeeris Limited',
    'Top End Energy Limited',
    'Labyrinth Resources Limited',
    'Locksley Resources Limited',
    'Taruga Minerals Limited',
    "Oliver's Real Food Limited",
    'Global Oil & Gas Limited',
    'Constellation Resources Limited',
    'Visioneering Technologies Inc',
    'M3 Mining Limited',
    'AQUIS Entertainment Limited',
    'Atrum Coal Limited',
    'Cipherpoint Limited',
    'Anagenics Limited',
    'DY6 Metals Limited',
    'Purifloh Limited',
    'VDM Group Limited',
    'Aeris Environmental Limited',
    'Betashares Euro ETF',
    'Elixinol Wellness Limited',
    'Patagonia Lithium Limited',
    'Wingara AG Limited',
    'FIN Resources Limited',
    'Zuleika Gold Limited',
    'Sprintex Limited',
    'Aurumin Limited',
    'Bellavista Resources Limited',
    'Equity Trustees Limited',
    'Miramar Resources Limited',
    'Aumake Limited',
    'Botala Energy Limited',
    'West Cobar Metals Limited',
    'LBT Innovations Limited',
    'Tempest Minerals Limited',
    'Cohiba Minerals Limited',
    'Victory Offices Limited',
    'Dominion Minerals Limited',
    'Doriemus Plc',
    'Epsilon Healthcare Limited',
    'Haranga Resources Limited',
    'Discovex Resources Limited',
    'Basin Energy Limited',
    'Kincora Copper Limited',
    'Global X Metal Securities Australia Limited',
    'Yowie Group Limited',
    'Vertex Minerals Limited',
    'Mpower Group Limited',
    'Terrain Minerals Limited',
    'Golden State Mining Limited',
    'Hydrocarbon Dynamics Limited',
    'Lightning Minerals Limited',
    'Future First Technologies Limited',
    'ZEUS Resources Limited',
    'Rocketdna Limited',
    'NT Minerals Limited',
    'Omnia Metals Group Limited',
    'Singular Health Group Limited',
    'Gibb River Diamonds Limited',
    'Kula Gold Limited',
    'Douugh Limited',
    'Island Pharmaceuticals Limited',
    'BMG Resources Limited',
    'Equinox Resources Limited',
    'OZZ Resources Limited',
    'Allegra Orthopaedics Limited',
    'Delorean Corporation Limited',
    'My Rewards International Limited',
    'White Energy Company Limited',
    'Sensera Limited',
    'Catalina Resources Limited',
    'TZ Limited',
    'Openlearning Limited',
    'Cooper Metals Limited',
    'Auric Mining Limited',
    'Mantle Minerals Limited',
    'Codrus Minerals Limited',
    'Dorsavi Limited',
    'Imperial Pacific Limited',
    'Austin Metals Limited',
    'The GO2 People Limited',
    'Enrg Elements Limited',
    'Noronex Limited',
    'Black Dragon Gold Corp',
    'Orexplore Technologies Limited',
    'Vaneck Global Carbon Credits ETF (Synthetic)',
    'Macro Metals Limited',
    'Equity Trustees Limited',
    'Jpmorgan GL Res En in EQ Active ETF (Managed Fund)',
    'Bryah Resources Limited',
    'Prospech Limited',
    'Tempus Resources Limited',
    'BTC Health Limited',
    'Carly Holdings Limited',
    'Nickelx Limited',
    'Energy Action Limited',
    'Ultima United Limited',
    'Discovery Alaska Limited',
    'SSH Group Limited',
    'Carbon Minerals Limited',
    'Rightcrowd Limited',
    'Forrestania Resources Limited',
    'AD1 Holdings Limited',
    'Audeara Limited',
    'Tek-Ocean Group Limited',
    'Connected Io Limited',
    'Cauldron Energy Limited',
    'BPM Minerals Limited',
    'NEX Metals Exploration Limited',
    'Range International Limited',
    'Empire Resources Limited',
    'Powerhouse Ventures Limited',
    'Careteq Limited',
    'Finder Energy Holdings Limited',
    'Global X Usd High Yield Bond ETF(Currency Hedged)',
    'Glennon Small Companies Limited',
    'Australia United Mining Limited',
    'Magnetic Resources NL',
    'Australian Gold and Copper Limited',
    'Australian Agricultural Projects Limited',
    'GREENHY2 Limited',
    'Cann Global Limited',
    'GPS Alliance Holdings Limited',
    'Terragen Holdings Limited',
    'Ozaurum Resources Limited',
    'Desoto Resources Limited',
    'ZINC of Ireland NL',
    'CHEMX Materials Limited',
    'EVE Health Group Limited',
    'Pantera Minerals Limited',
    'Equity Trustees Limited',
    'Redstone Resources Limited',
    'Mighty Kingdom Limited',
    'Protean Energy Limited',
    'Australian Potash Limited',
    'Spectur Limited',
    'Eneco Refresh Limited',
    'Dart Mining NL',
    'Osmond Resources Limited',
    'Health and Plant Protein Group Limited',
    'Equity Trustees Limited',
    'Hexagon Energy Materials Limited',
    'Nightingale Intelligent Systems Inc',
    'IPB Petroleum Limited',
    'Scout Security Limited',
    'Benjamin Hornigold Limited',
    'HITIQ Limited',
    'Adelong Gold Limited',
    'Aoris Int Fund (Class B) (Unhedged) (Managed Fund)',
    'Mithril Resources Limited',
    'Cullen Resources Limited',
    '8VI Holdings Limited',
    'Resolution Minerals Limited',
    'Albion Resources Limited',
    'Caprice Resources Limited',
    'Sipa Resources Limited',
    'Variscan Mines Limited',
    'Tasman Resources Limited',
    'Godolphin Resources Limited',
    'Alderan Resources Limited',
    'Alterra Limited',
    'Coolabah Metals Limited',
    'MTM Critical Metals Limited',
    'High-Tech Metals Limited',
    'Hiremii Limited',
    'Ronin Resources Limited',
    'Narryer Metals Limited',
    'Bindi Metals Limited',
    'Auris Minerals Limited',
    'Saferoads Holdings Limited',
    'Aurora Labs Limited',
    'Heavy Minerals Limited',
    'Analytica Limited',
    'Pivotal Systems Corporation',
    'Clara Resources Australia Limited',
    'Kneomedia Limited',
    'Opyl Limited',
    'Strategic Energy Resources Limited',
    'M8 Sustainable Limited',
    'Constellation Technologies Limited',
    'MRG Metals Limited',
    'Lykos Metals Limited',
    'MCS Services Limited',
    'International Equities Corporation Limited',
    'Traka Resources Limited',
    'First Au Limited',
    'Thomson Resources Limited',
    'Bastion Minerals Limited',
    'Summit Minerals Limited',
    'Nelson Resources Limited',
    'Norfolk Metals Limited',
    'E79 Gold Mines Limited',
    'Datadot Technology Limited',
    'Elmore Limited',
    'Kalgoorlie Gold Mining Limited',
    'Bubalus Resources Limited',
    'Equity Trustees Limited',
    'Metalsgrove Mining Limited',
    'Koonenberry Gold Limited',
    'The Calmer Co International Limited',
    'GAS2GRID Limited',
    'Nyrada Inc',
    'Love Group Global Limited',
    'Canterbury Resources Limited',
    'RBR Group Limited',
    'Black Mountain Energy Limited',
    'Betashares Global Shares ETF - Currency Hedged',
    'Sultan Resources Limited',
    'Skin Elements Limited',
    'Dragon Mountain Gold Limited',
    'Boadicea Resources Limited',
    'Uvre Limited',
    'Westar Resources Limited',
    'Ishares High Growth Esg ETF',
    'Ausmon Resources Limited',
    'Sacgasco Limited',
    'Great Northern Minerals Limited',
    'Xstate Resources Limited',
    'FAT Prophets Global High Conviction Hedge Fund',
    'Nucoal Resources Limited',
    'Hexima Limited',
    'Kaddy Limited',
    'TG Metals Limited',
    'Nickelsearch Limited',
    'Global X Usd Corporate Bond ETF (Currency Hedged)',
    'Dundas Minerals Limited',
    'Accent Resources NL',
    'Betashares Global Royalties ETF',
    'Optima Technology Group Limited',
    'Emperor Energy Limited',
    'Western Gold Resources Limited',
    'Heavy Rare EARTHS Limited',
    'Equity Trustees Limited',
    'Betashares Solar ETF',
    'Australian Bond Exchange Holdings Limited',
    'Redcastle Resources Limited',
    'TYMLEZ Group Limited',
    'Reedy Lagoon Corporation Limited',
    'Panther Metals Limited',
    'Activex Limited',
    'Cavalier Resources Limited',
    'Trigg Minerals Limited',
    'Simble Solutions Limited',
    'Remsense Technologies Limited',
    'REGENER8 Resources NL',
    'Harris Technology Group Limited',
    'Rocketboots Limited',
    'ZIMI Limited',
    'Timah Resources Limited',
    'Advance Metals Limited',
    'Exopharm Limited',
    'Equity Trustees Limited',
    'Mamba Exploration Limited',
    'I Synergy Group Limited',
    'Nexion Group Limited',
    'Sarama Resources Limited',
    'Middle Island Resources Limited',
    'Anatara Lifesciences Limited',
    'Bentley Capital Limited',
    'Perpetual Esg Australian Share Fund (Managed Fund)',
    'BPH Global Limited',
    'Carbine Resources Limited',
    'New Zealand Coastal Seafoods Limited',
    'Tali Digital Limited',
    'Peako Limited',
    'Acdc Metals Limited',
    'Golden Cross Resources Limited',
    'Sierra Nevada Gold Inc',
    'Pearl Gull Iron Limited',
    'DC Two Limited',
    'Nutritional Growth Solutions Limited',
    'Diablo Resources Limited',
    'Mec Resources Limited',
    'Global X Metal Securities Australia Limited',
    'Santa Fe Minerals Limited',
    'Avira Resources Limited',
    'Enterprise Metals Limited',
    'Ishares Future Tech Innovators ETF',
    '333D Limited',
    'Genesis Resources Limited',
    'Peak Minerals Limited',
    'Desert Metals Limited',
    'Global X Uranium ETF',
    'Icon Energy Limited',
    'Mount Burgess Mining NL',
    'Merchant House International Limited',
    'Techgen Metals Limited',
    'Propell Holdings Limited',
    'SQX Resources Limited',
    'KEY Petroleum Limited',
    'Lord Resources Limited',
    'Halo Food Co. Limited',
    'Holista Colltech Limited',
    'C29 Metals Limited',
    'Aurum Resources Limited',
    'Happy Valley Nutrition Limited',
    'Enova Mining Limited',
    'Intelicare Holdings Limited',
    'Eastern Metals Limited',
    'Culpeo Minerals Limited',
    'Octava Minerals Limited',
    'YPB Group Limited',
    'Forbidden Foods Limited',
    'Betashares Nasdaq 100 Yield MAX (Managed Fund)',
    'Perpetual Global Innovation Share (Managed Fund)',
    'Identitii Limited',
    'JAYEX Technology Limited',
    'Cosmo Metals Limited',
    'Global X S&P/ASX 200 Covered Call ETF',
    'Sagalio Energy Limited',
    'Global X Australia Ex Financials & Resources ETF',
    'Betashares Future of Payments ETF',
    'Betashares Metaverse ETF',
    'Killi Resources Limited',
    'Applyflow Limited',
    'VIP Gloves Limited',
    'Moho Resources Limited',
    'Dalaroo Metals Limited',
    'Inventis Limited',
    'Rincon Resources Limited',
    'Global X Green Metal Miners ETF',
    'Pinnacle Minerals Limited',
    'Oakajee Corporation Limited',
    'EMU NL',
    'Allup Silica Limited',
    'CYCLIQ Group Limited',
    'Regeneus Limited',
    'Betashares Future of Food ETF',
    'MT Malcolm Mines NL',
    'Milford Australian Absolute Growth (Hedge Fund)',
    'Oakridge International Limited',
    'TTA Holdings Limited',
    'Prominence Energy Limited',
    'Winchester Energy Limited',
    'Parkd Limited',
    'Betashares Video Games and Esports ETF',
    'Assetowl Limited',
    'Equity Story Group Limited',
    'Alice QUEEN Limited',
    'DMC Mining Limited',
    'DXN Limited',
    'Star Minerals Limited',
    'Orange Minerals NL',
    'Orion Equities Limited',
    'Ishares Balanced Esg ETF',
    'Global X Bloomberg Commodity ETF (Synthetic)',
    'Betashares Digital Health and Telemedicine ETF',
    'Aneka Tambang (Persero) TBK (PT)',
    'Armada Metals Limited',
    'Story-I Limited',
    'Mariner Corporation Limited',
    'Janus HDRSN ZR Trans Res Active ETF (Managed Fund)',
    'Wellfully Limited',
    'Kaili Resources Limited',
    'Cfoam Limited',
    'Raptis Group Limited',
    'Global X Global Carbon ETF (Synthetic)',
    'Invigor Group Limited',
    'Asaplus Resources Limited',
    'Global X Nasdaq 100 Covered Call ETF',
    'JPM US100Q EQ Prem Inc Active ETF (Managed Fund)',
    'Jpmorgan Climate CHG Sol Active ETF (Managed Fund)',
    'JPM US100Q EQ Prem Inc H Active ETF (Managed Fund)',
    'Equity Trustees Limited',
    'Catalano Seafood Limited',
    'JPM EQTY Prem Inc H Active ETF (Managed Fund)',
    'Jpmorgan Sustain Infra Active ETF (Managed Fund)',
    'Colortv Limited',
    'Munro Concentrated Global Growth (Managed Fund)',
    'Global X S&P 500 Covered Call ETF',
    'Equity Trustees Limited',
    'Betashares Online Retail and E-Commerce ETF',
    'ABRDN Sust Asian Opp Active ETF (Managed Fund)',
    'Janus Henderson GLB Sust Active ETF (Managed Fund)',
    'Equity Trustees Limited',
    'Global X US 100 ETF',
    'Bridge Saas Limited',
    'Laramide Resources Limited',
    'My Foodie BOX Limited',
    'Multistack International Limited',
    'Aurora Global Income Trust',
    'Queste Communications Limited',
    'Equity Trustees Limited',
    'Roots Sustainable Agricultural Technologies Limited',
    'Equity Trustees Limited',
    'Lawfinance Limited',
    'Janus Henderson Sust CR Active ETF (Managed Fund)',
    'Carlton Investments Limited',
    'EMU NL',
    'Sietel Limited',
    'Whitefield Industrials Limited', 'Cash - US Dollar'
                ]


                word_based_credits = ['PAYG Payable','Employer Contributions','Interest Received','Employer Contributions','Personal Non Concessional',
                                    'Personal Concessional', 'Other Contributions','Other Investment Income','Property Income','Forex Gain/Loss']

                #For matched values has to store as dictionary data structure
                matched_values = {}
                Link_notGenerated = []
                #Open the PDF_file Using PyPDF2
                pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
                
                #For using pdfplumber to get the matched values like page number , matched values data
                with pdfplumber.open(pdf_path)  as pdf:
                    for word in words_to_find:
                        matched_amount = None
                        matched_page_number = None
                        matched_word = None
                        for page_num, page in enumerate(pdf.pages):
                            if page_num <= 3:
                                lines = page.extract_text().split('\n')
                                for line in lines:
                                    
                                    if word in line:
                                        # data_values = re.findall(r'\((\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)', line)
                                        # print(data_values)
                                        data_values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', line)
                                    
                                        if data_values:
                                            if data_values[0] != 0:
                                                matched_amount = data_values[0]   # Extract the first value from the line
                                            
                                                matched_page_number = page_num
                                                matched_word = word
                                                break 
                                if matched_amount:
                                    break
                        if matched_amount:
                        
                            matched_values[word] = {
                                'value': matched_amount,
                                'page_number': matched_page_number,
                                'word': matched_word
                            }

                    #Create a new PDF using PyPDF2
                    pdf_writer = PdfFileWriter()

                    #Copy the existing pages to the new PDF
                    for page_num in range(pdf_reader.getNumPages()):
                        current_page = pdf_reader.getPage(page_num)
                        pdf_writer.addPage(current_page)

                    
                    for word in words_to_find:
                        if  word in matched_values and matched_values[word]['value'] != '0.00' :         
                            #To find or find the word and get dimension of the word using fitz module
                            doc = fitz.open(pdf_path)
                            page = doc[matched_values[word]['page_number']]
                            #This for pdfwriter.addlink to place the link to matched word page
                            page_no_to_palce_link = matched_values[word]['page_number']

                            # Search for a specific word and retrieve its coordinates
                            keyword_matched_amount = matched_values[word]['value']
                            matched_word_string = matched_values[word]['word']
                        
                        
                    

                            if matched_word_string == 'Benefits accrued as a result of operations before income tax':
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'Benefits accrued as a result of operations'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[-1]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1,1,1]
                                                            )
                                                            break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(word)
                                            pass    

                            elif matched_word_string == 'Income Tax Expense' or  matched_word_string == 'Income Tax Refundable':
                                
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'CURRENT TAX OR REFUND'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[-1]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1,1,1]
                                                            )
                                                            break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(word)
                                            pass    

                            elif matched_word_string == 'Trust Distributions' or matched_word_string == 'Dividends Received':
                                            
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            if matched_word_string == 'Trust Distributions':
                                                value_to_find = 'Distribution Reconciliation Report'
                                            else:
                                                value_to_find = 'Dividend Reconciliation Report'

                                            subsequent_word = 'TOTAL'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[0]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1,1,1]
                                                            )
                                                            break
                                        except:
                                            Link_notGenerated.append(word)
                                            pass 
                            
                            elif matched_word_string == 'Income Tax Payable':
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Statement of Taxable Income'
                                            subsequent_word = 'AMOUNT DUE OR REFUNDABLE'

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            page = pdf.pages[matched_goto_pagenumber]
                                            
                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if subsequent_word in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                                    if data:

                                                        matched_data = data[-1]
                                                        doc = fitz.open(pdf_path)
                                                        matched_page = doc[matched_goto_pagenumber]

                                                        keyword = matched_data

                                                        word_instances = matched_page.search_for(keyword)
                                                        if len(word_instances) > 0:
                                                            x,y,x1,y1 = word_instances[-1]
                                                            page_height = matched_page.rect.height

                                                            new_y = page_height - y1
                                                            pdf_writer.addLink(
                                                                matched_goto_pagenumber,
                                                                page_no_to_palce_link,
                                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                border=[1,1,1]
                                                            )
                                                            break
                                        except Exception as e:
                                    
                                            Link_notGenerated.append(word)
                                            pass    
                            
                            elif matched_word_string in ['Managed Investments (Australian)', 'Managed Investments (Overseas)' , 'Shares in Listed Companies (Australian)' ,
                                                        'Shares in Listed Companies (Overseas)', 'Shares in Unlisted Private Companies (Overseas)' , 'Units in Listed Unit Trusts (Australian)',
                                                        'Units in Unlisted Unit Trusts (Australian)' , 'Plant and Equipment (at written down value) - Unitised',
                                                        'Real Estate Properties ( Australian - Residential)' ,'Derivatives (Options, Hybrids, Future Contracts)',
                                                        'Other Assets', 'Loans to Associated Entities (In house loans) - Unitised',
                                                        'Stapled Securities' ,'Mortgage Loans (Australian)' , 'Fixed Interest Securities (Australian) - Unitised',
                                                        'Shares in Unlisted Private Companies (Australian)','Units in Listed Trusts (Australian)',
                                                        
                                                        
    'BHP Group Limited',
    'Commonwealth Bank of Australia','CSL Limited','National Australia Bank Limited','Westpac Banking Corporation','ANZ Group Holdings Limited',
    'Woodside Energy Group Limited','Macquarie Group Limited','Fortescue Metals Group Limited','Wesfarmers Limited','Woolworths Group Limited',
    'Telstra Group Limited','Goodman Group','Transurban Group','RIO Tinto Limited','Aristocrat Leisure Limited','Santos Limited','Wisetech Global Limited',
    'Newcrest Mining Limited','QBE Insurance Group Limited','Coles Group Limited','REA Group Limited','Brambles Limited','James Hardie Industries Plc',
    'Xero Limited','Cochlear Limited','Suncorp Group Limited','SOUTH32 Limited','Sonic Healthcare Limited','Computershare Limited','Origin Energy Limited',
    'Scentre Group','Insurance Australia Group Limited','Pilbara Minerals Limited','Mineral Resources Limited','Northern Star Resources Limited','Reece Limited',
    'Vanguard Australian Shares INDEX ETF','Fisher & Paykel Healthcare Corporation Limited','Ramsay Health Care Limited','Washington H Soul Pattinson & Company Limited',
    'ASX Limited','The Lottery Corporation Limited','APA Group','Resmed Inc','Auckland International Airport Limited','Carsales.com Limited','Qantas Airways Limited',
    'TPG Telecom Limited','Seven Group Holdings Limited','Stockland','IGO Limited','Endeavour Group Limited','Medibank Private Limited','Amcor Plc','Gold Corporation',
    'Bluescope Steel Limited','Mirvac Group','Worley Limited','Allkem Limited','Atlas Arteria','Treasury Wine Estates Limited','Australian Foundation Investment Company Limited',
    'Spark New Zealand Limited','Vicinity Centres','Dexus','Seek Limited','Ampol Limited','Mercury NZ Limited','GPT Group','Pro Medicus Limited','Infratil Limited',
    'AGL Energy Limited','Orica Limited','Yancoal Australia Limited','Idp Education Limited','Magellan Global Fund (Open Class) (Managed Fund)','NEXTDC Limited',
    'Lynas Rare EARTHS Limited','Evolution Mining Limited','Aurizon Holdings Limited','Ebos Group Limited','Argo Investments Limited','Meridian Energy Limited',
    'Altium Limited','Vanguard MSCI INDEX International Shares ETF','Ishares S&P 500 ETF','Liontown Resources Limited','Cleanaway Waste Management Limited','Steadfast Group Limited',
    'Incitec Pivot Limited','Als Limited','Whitehaven Coal Limited','QUBE Holdings Limited','Bendigo and Adelaide Bank Limited','Lendlease Group','Boral Limited',
    'Charter Hall Group','JB Hi-Fi Limited','Technology One Limited','New Hope Corporation Limited','Viva Energy Group Limited',"Domino's PIZZA Enterprises Limited",
    'SPDR S&P/ASX 200 Fund','Harvey Norman Holdings Limited','Challenger Limited','Flight Centre Travel Group Limited','GQG Partners Inc','Ishares Core S&P/ASX 200 ETF',
    'Premier Investments Limited','Brickworks Limited','Eagers Automotive Limited','Vaneck MSCI International Quality ETF','Nib Holdings Limited','Bank of Queensland Limited',
    'Netwealth Group Limited','Metcash Limited','Vanguard US Total Market Shares INDEX ETF','Iluka Resources Limited','Beach Energy Limited','Fletcher Building Limited',
    'TELIX Pharmaceuticals Limited','AMP Limited','Breville Group Limited','Betashares Nasdaq 100 ETF','The a2 Milk Company Limited','AUB Group Limited','Nine Entertainment Co. Holdings Limited',
    'Reliance Worldwide Corporation Limited','Chorus Limited','Betashares Australia 200 ETF','National Storage REIT','Champion Iron Limited','Betashares Australian High Interest Cash ETF',
    'Alumina Limited','Ansell Limited','Global X Metal Securities Australia Limited','Vanguard Australian Shares High Yield ETF','Orora Limited','Sandfire Resources Limited',
    'Sims Limited','Super Retail Group Limited','Ishares Global 100 ETF','Webjet Limited','Downer Edi Limited','CSR Limited','ARB Corporation Limited',
    'Corporate Travel Management Limited','Block Inc','AVZ Minerals Limited','Zimplats Holdings Limited','Nickel Industries Limited','Coronado Global Resources Inc',
    'Vanguard All-World Ex-US Shares INDEX ETF','Betashares Global Sustainability Leaders ETF','HUB24 Limited','Stanmore Resources Limited','Perseus Mining Limited',
    'Charter Hall Long Wale REIT','BSP Financial Group Limited','Homeco Daily Needs REIT','Tabcorp Holdings Limited','Paladin Energy Limited','Magellan Global Fund',
    'National Australia Bank Limited','Region Group','Air New Zealand Limited','Vanguard Australian Property Securities INDEX ETF','Vanguard MSCI INDEX International Shares (Hedged) ETF',
    'Lovisa Holdings Limited','Perpetual Limited','Genesis Energy Limited','Domain Holdings Australia Limited','BWP Trust','Ventia Services Group Limited',
    'Hyperion GBL Growth Companies Fund (Managed Fund)','Deterra Royalties Limited','Bapcor Limited','De Grey Mining Limited','Virgin Money Uk Plc',
    'Summerset Group Holdings Limited','Vanguard Diversified High Growth INDEX ETF','Pexa Group Limited','National Australia Bank Limited','Ishares Core Composite Bond ETF',
    'Betashares Active Australian Hybrids Fund (Managed Fund)','Charter Hall Retail REIT','Nufarm Limited','National Australia Bank Limited','Centuria Industrial REIT',
    'EVT Limited','Contact Energy Limited','Gold Road Resources Limited','Vaneck Australian EQUAL Weight ETF','HMC Capital Limited','Megaport Limited',
    'Pinnacle Investment Management Group Limited','Bellevue Gold Limited','Wam Leaders Limited','Growthpoint Properties Australia','Lifestyle Communities Limited',
    'WAM Capital Limited','IPH Limited','Invocare Limited','L1 Long Short Fund Limited','Commonwealth Bank of Australia','LIFE360 Inc','Metrics Master Income Trust',
    'Westpac Banking Corporation','PSC Insurance Group Limited','Westpac Banking Corporation','Commonwealth Bank of Australia','Johns LYNG Group Limited',
    'Kelsian Group Limited','Westpac Banking Corporation','MFF Capital Investments Limited','Magellan Financial Group Limited','Graincorp Limited',
    'APM Human Services International Limited','G.U.D. Holdings Limited','Waypoint REIT','Insignia Financial Limited','Commonwealth Bank of Australia','Capricorn Metals Limited',
    'Ingenia Communities Group','Australia and New Zealand Banking Group Limited','Genesis Minerals Limited','Healius Limited','Abacus Storage King','Vanguard Australian Fixed Interest INDEX ETF',
    'The Star Entertainment Group Limited','Neuren Pharmaceuticals Limited','Commonwealth Bank of Australia','Macquarie Technology Group Limited','Dicker Data Limited',
    'Skycity Entertainment Group Limited','Commonwealth Bank of Australia','Mader Group Limited','Westpac Banking Corporation','Australia and New Zealand Banking Group Limited',
    'Australia and New Zealand Banking Group Limited','United Malt Group Limited','Westpac Banking Corporation','Chalice Mining Limited','Credit Corp Group Limited',
    'Adbri Limited','Commonwealth Bank of Australia','Codan Limited','BKI Investment Company Limited','Monadelphous Group Limited','Emerald Resources NL',
    'Dalrymple Bay Infrastructure Limited','Light & Wonder Inc','Ramelius Resources Limited','Karoon Energy Limited','REDOX Limited','Costa Group Holdings Limited',
    'Ishares Global Healthcare ETF','Australia and New Zealand Banking Group Limited','Siteminder Limited','Arena REIT','Inghams Group Limited','Cromwell Property Group',
    'Nanosonics Limited','Sayona Mining Limited','Resolution Cap Global Prop Sec (Managed Fund)','Betashares Australian Sustainability Leaders ETF','Mcmillan Shakespeare Limited',
    'NRW Holdings Limited','Latitude Group Holdings Limited','Regis Resources Limited','Iress Limited','Australian United Investment Company Limited','Centuria Capital Group',
    'Helia Group Limited','Objective Corporation Limited','Commonwealth Bank of Australia','Boss Energy Limited','Accent Group Limited','Liberty Financial Group',
    'Collins Foods Limited','Ishares S&P 500 Aud Hedged ETF','Data#3 Limited','Heartland Group Holdings Limited','Betashares Australian Bank Senior Floating Rate Bond ETF',
    'Leo Lithium Limited','Smartgroup Corporation Limited','Hansen Technologies Limited','Audinate Group Limited','Maas Group Holdings Limited','PWR Holdings Limited',
    'Cettire Limited','Abacus Group','AZURE Minerals Limited','Charter Hall Social Infrastructure REIT','Macquarie Group Limited','Diversified United Investment Limited',
    'Elders Limited','Polynovo Limited','Judo Capital Holdings Limited','Vulcan Steel Limited','Nick Scali Limited','Jumbo Interactive Limited','Briscoe Group Australasia Limited',
    'Clinuvel Pharmaceuticals Limited','Strike Energy Limited','Australia and New Zealand Banking Group Limited','Macquarie Group Limited','National Australia Bank Limited',
    'SG Fleet Group Limited','Vanguard Australian Government Bond INDEX ETF','News Corporation','G8 Education Limited','Tuas Limited','Bega Cheese Limited',
    'Silver Lake Resources Limited','Energy Resources of Australia Limited','Dexus Industria REIT','Platinum Asset Management Limited','Ishares MSCI Emerging Markets ETF',
    'Aussie Broadband Limited','West African Resources Limited','Adriatic Metals Plc','Alpha Hpa Limited','Australian Agricultural Company Limited','Vanguard International Fixed Interest INDEX (Hedged) ETF',
    'Vaneck Australian Subordinated Debt ETF','Sigma Healthcare Limited','Core Lithium Limited','Temple & Webster Group Limited','Latin Resources Limited',
    'Healthco Healthcare and Wellness REIT','SPDR S&P/ASX 50 Fund','Ma Financial Group Limited','IMDEX Limited','Rural Funds Group','Vaneck Ftse Global Infrastructure (Hedged) ETF',
    'Resolute Mining Limited','Ooh!Media Limited','Vanguard Global Aggregate Bond INDEX (Hedged) ETF','Plato Income Maximiser Limited','RED 5 Limited','Ishares Europe ETF',
    'Vanguard MSCI Australian Small Companies INDEX ETF','Estia Health Limited','Carlton Investments Limited','PM Capital Global Opportunities Fund Limited','Westgold Resources Limited',
    'Macquarie Group Limited','Centuria Office REIT','Fleetpartners Group Limited','Tourism Holdings Rentals Limited','Betashares Global Cybersecurity ETF',
    'Activex Ardea Real Outcome Bond Fund (Managed Fund)','Weebit Nano Limited','Regis Healthcare Limited','SILEX Systems Limited','Djerriwarrh Investments Limited',
    'Macquarie Group Limited','Vanguard Ftse Emerging Markets Shares ETF','Nanuk New World Fund (Managed Fund)','Tyro Payments Limited','Vanguard Ethically Conscious International Shares INDEX ETF',
    'Vaneck MSCI International Quality (Hedged) ETF','CALIX Limited','Ishares Asia 50 ETF','Winton Land Limited','EQT Holdings Limited','Perenti Limited','Integral Diagnostics Limited',
    'Vanguard Diversified Growth INDEX ETF','Qualitas Limited','Wam Global Limited','Ishares Core MSCI World Ex Australia Esg ETF','Austal Limited','Macquarie Bank Limited',
    'Ishares Core Cash ETF','Magellan Infrastructure Fund (Currency Hedged)(Managed Fund)','Fineos Corporation Holdings Plc','Ridley Corporation Limited','Link Administration Holdings Limited',
    'Deep Yellow Limited','Unibail-Rodamco-Westfield','Macquarie Bank Limited','KKR Credit Income Fund','Vaneck Morningstar Wide Moat ETF','Infomedia Limited',
    'Vanguard Australian Corp Fixed Interest INDEX ETF','Vanguard Diversified Balanced INDEX ETF','Regal Partners Limited','Vaneck Australian Floating Rate ETF',
    'Vaneck Australian Property ETF','NB Global Corporate Income Trust','Global X Battery Tech & Lithium ETF','Supply Network Limited','Ishares Government Inflation ETF',
    'Omni Bridgeway Limited','Australian Clinical Labs Limited','Qualitas Real Estate Income Fund','Whitefield Industrials Limited','Hotel Property Investments',
    'Pepper Money Limited','Vanguard Global Value Equity Active ETF (Managed Fund)','Vulcan Energy Resources Limited','Regal Investment Fund','Peet Limited',
    'Hutchison Telecommunications (Australia) Limited','Pacific Current Group Limited','Kogan.com Limited','Cobram Estate Olives Limited','Service Stream Limited',
    'Mirrabooka Investments Limited','Ophir High Conviction Fund','Hearts and Minds Investments Limited','Develop Global Limited','Betashares Australian Investment Grade Corporate Bond ETF',
    'KMD Brands Limited','Myer Holdings Limited','Metrics Income Opportunities Trust','Novonix Limited','Tietto Minerals Limited','Brainchip Holdings Limited',
    'Restaurant Brands New Zealand Limited','Arafura Rare EARTHS Limited','Mount Gibson Iron Limited','Vgi Partners Global Investments Limited','Ishares S&P/ASX 20 ETF',
    'GWA Group Limited','Propel Funeral Partners Limited','Autosports Group Limited','Global X US Treasury Bond ETF (Currency Hedged)','Bendigo and Adelaide Bank Limited','Grange Resources Limited',
    'Alliance Aviation Services Limited','Insurance Australia Group Limited','Helloworld Travel Limited','NUIX Limited','Select Harvests Limited','Mma Offshore Limited',
    'Oceania Healthcare Limited','Betashares Westn Asset Aus Bond Fund (Managed Fund)','Pointsbet Holdings Limited','Australian Ethical Investment Limited','Ishares MSCI Japan ETF',
    'SPDR S&P/ASX 200 Listed Property Fund','Ioneer Limited','Gryphon Capital Income Trust','Betashares Asia Technology Tigers ETF','Monash Ivf Group Limited',
    'Betashares Australian Government Bond ETF','Partners Group Global Income Fund','Future Generation Australia Limited','Future Generation Global Limited','Ishares S&P Small-Cap ETF',
    'Perpetual Equity Investment Company Limited','Seven West Media Limited','Betashares Gold Bullion ETF - Currency Hedged','Magellan High Conviction Trust (Managed Fund)',
    'Talga Group Limited','Betashares Ftse 100 ETF','Imugene Limited','Patriot Battery Metals Inc','Peter Warren Automotive Holdings Limited','OFX Group Limited','Boart Longyear Group Limited',
    'Vaneck Gold Miners ETF','Predictive Discovery Limited','Betashares Ftse Rafi Australia 200 ETF','Ricegrowers Limited','Cedar Woods Properties Limited','Alphinity Global Equity Fund (Managed Fund)',
    'Serko Limited','SSR Mining Inc','Pengana Private Equity Trust','Resimac Group Limited','Ishares MSCI Eafe ETF','SPDR Dow Jones Global Real Estate Esg Fund',
    'Gentrack Group Limited','Ishares Treasury ETF','Australian Finance Group Limited','Delta Lithium Limited','Perpetual Credit Income Trust','Suncorp Group Limited',
    'Alkane Resources Limited','Beacon Lighting Group Limited','Lycopodium Limited','Mayne Pharma Group Limited','Bank of Queensland Limited','EML Payments Limited',
    'Betashares Aus Top 20 Equity Yield MAX Fund (Managed Fund)','Readytech Holdings Limited','Challenger Limited','SPDR MSCI Australia Select High Dividend Yield Fund',
    'Suncorp Group Limited','GR Engineering Services Limited','Betashares Geared Australian Equity Fund (Hedge Fund)','Platinum Capital Limited','Om Holdings Limited',
    'Airlie Australian Share Fund (Managed Fund)','Chrysos Corporation Limited','Betashares Global Quality Leaders ETF','Argo Global Listed Infrastructure Limited',
    'Janus Henderson Group Plc','Vanguard Ethically Conscious Australian Shares ETF','Global Lithium Resources Limited','Vaneck Australian Resources ETF',
    'Suncorp Group Limited','Ipd Group Limited','Jupiter Mines Limited','Syrah Resources Limited','Meteoric Resources NL','Regal Asian Investments Limited',
    'Betashares Global Sustainability Leaders ETF - CH','Ram Essential Services Property Fund','Lindsay Australia Limited','Mesoblast Limited','Centaurus Metals Limited',
    'SRG Global Limited','Smartpay Holdings Limited','Terracom Limited','SPDR S&P Global Dividend Fund','Clearview Wealth Limited','Steamships Trading Company Limited',
    'Vanguard Global Infrastructure INDEX ETF','29METALS Limited','Challenger Limited','Mystate Limited','Macmahon Holdings Limited','Renascor Resources Limited',
    'Bank of Queensland Limited','Aft Pharmaceuticals Limited','Vanguard Ftse Asia Ex Japan Shares INDEX ETF','Impedimed Limited','Michael Hill International Limited',
    'Antipodes Global Shares (Quoted Managed Fund)','Vista Group International Limited','Dexus Convenience Retail REIT','Kingsgate Consolidated Limited','BCI Minerals Limited',
    'Bravura Solutions Limited','Navigator Global Investments Limited','Superloop Limited','Rpmglobal Holdings Limited','DDH1 Limited','SPDR S&P World Ex Australia Carbon Control Fund',
    'Bell Financial Group Limited','Emeco Holdings Limited','Duratec Limited','Argosy Minerals Limited','Ainsworth Game Technology Limited','K & S Corporation Limited',
    'Global X Fang+ ETF','Lindian Resources Limited','GDI Property Group','Anteris Technologies Limited','Praemium Limited','Wam Microcap Limited','Global X Morningstar Global Technology ETF',
    'Immutep Limited','Bendigo and Adelaide Bank Limited','Sky Network Television Limited','Platinum International Fund (Quoted Managed Hedge Fund)','WCM Quality Global Growth Fund (Quoted Managed Fund)',
    'Ive Group Limited','Aspen Group','Russell Investments Australian Responsible Investment ETF','Ishares Global 100 Aud Hedged ETF','Ishares China Large-Cap ETF',
    'Avita Medical Inc',"Fonterra Shareholders' Fund",'Burgundy Diamond Mines Limited','Carindale Property Trust','3P Learning Limited','Platinum Asia Investments Limited',
    'Lake Resources N.L.','Amcil Limited','Cooper Energy Limited','Audio Pixels Holdings Limited','Aroa Biosurgery Limited','Lotus Resources Limited','Bannerman Energy Limited',
    'Universal Store Holdings Limited','Servcorp Limited','Ishares S&P/ASX DIV Opportunities Esg Screened ETF','AMP Limited','Australian Unity Limited','United Overseas Australia Limited',
    'Baby Bunting Group Limited','Australian Strategic Materials Limited','Neometals Limited','QORIA Limited','Botanix Pharmaceuticals Limited',
    'Turners Automotive Group Limited','Lynch Group Holdings Limited','ZIP Co Limited','CVC Limited','Betashares Sustainability Leaders DVRSFD Bond ETF - Cur HDG',
    'Carnarvon Energy Limited','Betashares Australian Strong Bear (Hedge Fund)','4DS Memory Limited','Ishares Edge MSCI World Minimum Volatility ETF',
    'Betashares Nasdaq 100 ETF - Currency Hedged','Clarity Pharmaceuticals Limited','Pengana International Equities Limited','Synlait Milk Limited',
    'Red Hill Minerals Limited','Ramsay Health Care Limited','Betashares Australian Major Bank Hybrids INDEX ETF','Catapult Group International Limited',
    'Bank of Queensland Limited','Arn Media Limited','Ardent Leisure Group Limited','Solvar Limited','Garda Property Group','Vaneck Australian Corporate Bond Plus ETF',
    'Pantoro Limited','Generation Development Group Limited','Vanguard MSCI International Small Companies INDEX ETF','Piedmont Lithium Inc','Strandline Resources Limited',
    'Russell Investments Australian Select Corporate Bond ETF','Betashares Diversified All Growth ETF','Galan Lithium Limited','Greenx Metals Limited',
    'Bigtincan Holdings Limited','COG Financial Services Limited','Ishares Enhanced Cash ETF','EBR Systems Inc','Spartan Resources Limited','Metals X Limited',
    'Sovereign Metals Limited','Base Resources Limited','Melbana Energy Limited','Duxton Water Limited','Auswide Bank Limited','Adairs Limited','Horizon Oil Limited',
    'Brockman Mining Limited','Ishares S&P Mid-Cap ETF','Appen Limited','Tamboran Resources Limited','Betashares US EQY Strong Bear - CH (Hedge Fund)',
    'Winsome Resources Limited','Russell Investments High Dividend Australian Shares ETF','Cogstate Limited','Silver Mines Limited','DGL Group Limited',
    'Atlantic Lithium Limited','Loftus Peak Global Disruption Fund (Managed Fund)','Elanor Commercial Property Fund','Wildcat Resources Limited',
    'Acrow Formwork and Construction Services Limited','Pact Group Holdings Limited','Betashares Australian Ex-20 Portfolio Diversifier ETF','Ishares Core Global Corporate Bond(Aud Hedged) ETF',
    'Vaneck Ftse International Property (Hedged) ETF','Vanguard Ftse Europe Shares ETF','Global X Robo Global Robotics & Automation ETF','Betashares Australian Composite Bond ETF',
    'Schaffer Corporation Limited','Firefinch Limited','Cyclopharm Limited','Orecorp Limited','Nufarm Finance (NZ) Limited','Ishares Core MSCI World Ex Aus Esg (Aud Hed) ETF',
    'Wam Research Limited','WCM Global Growth Limited','Kina Securities Limited','Capitol Health Limited','Betashares S&P 500 EQUAL Weight ETF','Close the Loop Limited',
    'Pacific Smiles Group Limited','Elanor Investors Group','Trajan Group Holdings Limited','Cadence Capital Limited','Iperionx Limited','Humm Group Limited',
    '4DMEDICAL Limited','Bowen Coking Coal Limited','PYC Therapeutics Limited','US Masters Residential Property Fund','Civmec Limited','Tower Limited',
    'Vitura Health Limited','Fidelity Global Emerging Markets Fund (Managed Fund)','Probiotec Limited','Ishares Global Consumer Staples ETF','Musgrave Minerals Limited',
    'Australian Unity Office Fund','The Reject Shop Limited','Vanguard Diversified Conservative INDEX ETF','Peoplein Limited','Magnetic Resources NL','QV Equities Limited',
    'WA1 Resources Limited','Newmark Property REIT','Southern Cross Electrical Engineering Limited','Betashares Global Energy Companies ETF - Currency Hedged',
    'SYMBIO Holdings Limited','DUG Technology Limited','Wam Alternative Assets Limited','SPDR S&P World Ex Aus Carbon Control (Hedged) Fund','Kelly Partners Group Holdings Limited',
    'Genusplus Group Limited','Vanguard MSCI Australian Large Companies INDEX ETF','Invictus Energy Limited','Global Value Fund Limited','Vaneck MSCI International Value ETF',
    'Big River Industries Limited','Atturra Limited','Quantum Graphite Limited','Betashares S&P/ASX Australian Technology ETF','Iodm Limited','Betashares Global Robotics and Artificial Intelligence ETF',
    'Opthea Limited','Volpara Health Technologies Limited','Vaneck MSCI Intl Small Companies Quality ETF','Wotso Property','Vaneck S&P/ASX Midcap ETF',
    'A2B Australia Limited','GENEX Power Limited','Barrow Hanley Global Share Fund (Managed Fund)','Bathurst Resources Limited','Fleetwood Limited','Paradigm Biopharmaceuticals Limited',
    'Vaneck Australian Banks ETF','Sheffield Resources Limited','Wam Strategic Value Limited','Fiducian Group Limited','Dropsuite Limited','Bailador Technology Investments Limited',
    'Southern Cross Media Group Limited','LGI Limited','Betashares Australian Dividend Harvester Fund (Managed Fund)','MACH7 Technologies Limited','FENIX Resources Limited',
    'Betashares Australian Resources Sector ETF','Anson Resources Limited','Berkeley Energia Limited','Munro Global Growth Fund (Hedge Fund)','Silk Laser Australia Limited',
    'Nexted Group Limited','Clover Corporation Limited','Droneshield Limited','Betashares Geared US Equity Fund Currency Hedged (Hedgefund)','Betashares Crude Oil INDEX ETF-Currency Hedged (Synthetic)',
    'Carnaby Resources Limited','Comet Ridge Limited','Tribune Resources Limited','PRT Company Limited','Tesserent Limited','ZETA Resources Limited','Wagners Holding Company Limited',
    'Finbar Group Limited','Highfield Resources Limited','Energy One Limited','Avjennings Limited','Lunnon Metals Limited','Redbubble Limited','Betashares Climate Change Innovation ETF',
    'Ora Banda Mining Limited','XRF Scientific Limited','Camplify Holdings Limited','Task Group Holdings Limited','EUROZ Hartleys Group Limited','Playside Studios Limited',
    'Northern Minerals Limited','Frontier Digital Ventures Limited SPONSORED','Aeris Resources Limited','Experience Co Limited','Iris Metals Limited','Vaneck MSCI International Sustainable Equity ETF',
    'Hot Chili Limited','Betashares Global Healthcare ETF - Currency Hedged','ST Barbara Limited','Aura Energy Limited','Morningstar International Shares Active ETF (Managed Fund)',
    'Austin Engineering Limited','NZME Limited','Motorcycle Holdings Limited','Aic Mines Limited','Nobleoak Life Limited','Ci Resources Limited','Xanadu Mines Limited',
    'Helios Energy Limited','Alcidion Group Limited','Reef Casino Trust','Ishares Edge MSCI World Multifactor ETF','Shaver Shop Group Limited','Danakali Limited',
    'SPDR S&P 500 ETF Trust','Peninsula Energy Limited','Waterco Limited','Vanguard International Credit Securities INDEX (Hedged) ETF','Vaneck Emerging Inc Opportunities Active ETF (Managed Fund)',
    'Ishares MSCI South Korea ETF','Vaneck MSCI Australian Sustainable Equity ETF','Alligator Energy Limited','Betashares S&P 500 Yield Maximiser Fund (Managed Fund)',
    'Electro Optic Systems Holdings Limited','Eroad Limited','Encounter Resources Limited','Russell Investments Australian Government Bond ETF','SPDR S&P/ASX 200 Resources Fund',
    'Betashares US Treasury Bond 20+YR ETF - CCY Hedged','Lithium Power International Limited','Enero Group Limited','Capral Limited','360 Capital Group','Nexgen Energy (Canada) Limited',
    'Global X Metal Securities Australia Limited','Shape Australia Corporation Limited','Silk Logistics Holdings Limited','Next Science Limited','Ishares Global High Yield Bond (Aud Hedged) ETF',
    'Oneview Healthcare Plc','Paragon Care Limited','Aurelia Metals Limited','Cash Converters International','Jervois Global Limited','Cosol Limited','Dreadnought Resources Limited',
    'Pancontinental Energy NL','Conrad Asia Energy Limited','Healthia Limited','Resource Development Group Limited','Kiland Limited','Bubs Australia Limited',
    'Maxiparts Limited','Global Data Centre Group','88 Energy Limited','Eureka Group Holdings Limited','Dacian Gold Limited','Tribeca Global Natural Resources Limited',
    'QANTM Intellectual Property Limited','Race Oncology Limited','Hastings Technology Metals Limited','DEVEX Resources Limited','Emvision Medical Devices Limited',
    'Latitude Group Holdings Limited','Bougainville Copper Limited','Ten Sixty Four Limited','Incannex Healthcare Limited','AMA Group Limited','Sunland Group Limited',
    'Gowing Bros Limited','Forager Australian Shares Fund','Red Hawk Mining Limited','Australian Vanadium Limited','5E Advanced Materials Inc','Viva Leisure Limited',
    'Murray Cod Australia Limited','Medadvisor Limited','Cti Logistics Limited','Cokal Limited','Ardea Resources Limited','Ishares S&P/ASX Small Ordinaries ETF',
    'Queensland Pacific Metals Limited','Retail Food Group Limited','Elevate Uranium Limited','Recce Pharmaceuticals Limited','Betashares Global Agriculture ETF - Currency Hedged',
    'Ansarada Group Limited','Ishares Core MSCI Australia Esg ETF','Pengana Capital Group Limited','FSA Group Limited','Betashares Martin Currie Em Fund (Managed Fund)',
    'Hillgrove Resources Limited','Rubicon Water Limited','Ishares Core Corporate Bond ETF','Cobalt Blue Holdings Limited','Saunders International Limited',
    'Hipages Group Holdings Limited','Smart Parking Limited','Peak Rare EARTHS Limited','EQ Resources Limited','Talon Energy Limited','Betashares U.S. Dollar ETF',
    'Archer Materials Limited','REX Minerals Limited','Lark Distilling Co. Limited','SPDR S&P/ASX 200 Financials Ex A-REIT Fund','Clime Capital Limited',
    'Newfield Resources Limited','Regional Express Holdings Limited','Magellan Global Equities Fund Currency Hedged (Managed Fund)','City Chic Collective Limited',
    'Global X Semiconductor ETF','Essential Metals Limited','Spheria Emerging Companies Limited','Orion Minerals Limited','Vaneck China New Economy ETF','Ariadne Australia Limited',
    'CD Private Equity Fund Iii','Empire Energy Group Limited','Vaneck Global Clean Energy ETF','Panoramic Resources Limited','Group 6 Metals Limited','Legend Mining Limited',
    'Janison Education Group Limited','Green Technology Metals Limited','Global X Copper Miners ETF','Catalyst Metals Limited','Altech Batteries Limited SPONSORED',
    'Magnis Energy Technologies Limited','Intelligent Investor Aus Equity Growth Fund (Managed Fund)','Energy World Corporation Limited','Embark Early Education Limited',
    'Coventry Group Limited','Engenco Limited','Fidelity Global Demographics Fund (Managed Fund)','Microba Life Sciences Limited','Minerals 260 Limited',
    'Proteomics International Laboratories Limited','E&P Financial Group Limited','American West Metals Limited','Mindax Limited','Shine Justice Limited',
    'Betmakers Technology Group Limited','PPK Group Limited','Calidus Resources Limited','Black Rock Mining Limited','European Metals Holdings Limited','Image Resources NL',
    'Platinum Asia Fund (Quoted Managed Hedge Fund)','Legacy Iron Ore Limited','Australian Vintage Limited','Step One Clothing Limited','SDI Limited',
    'Acusensus Limited','Ikegps Group Limited','Santana Minerals Limited','Jindalee Resources Limited','Globe International Limited','Imricor Medical Systems Inc',
    'Envirosuite Limited','Brisbane Broncos Limited','Beacon Minerals Limited','European Lithium Limited','Fluence Corporation Limited','New Zealand King Salmon Investments Limited',
    'DOTZ Nano Limited','Firstwave Cloud Technology Limited','Laserbond Limited','Korvest Limited','Structural Monitoring Systems Plc','Naos Small Cap Opportunities Company Limited',
    'Sezzle Inc','Ashley Services Group Limited','Synertec Corporation Limited','Freelancer Limited','The Market Herald Limited','Bisalloy Steel Group Limited',
    'Theta Gold Mines Limited','Byron Energy Limited','HAZER Group Limited','Caravel Minerals Limited','HEJAZ Equities Fund (Managed Fund)','Thorney Opportunities Limited',
    'Metro Mining Limited','Adore Beauty Group Limited','Otto Energy Limited','Andromeda Metals Limited','Shriro Holdings Limited','Frontier Energy Limited',
    'Global X Euro STOXX 50 ETF','Kinetiko Energy Limited','Sandon Capital Investments Limited','Tivan Limited','Challenger Gold Limited','Sunrise Energy Metals Limited',
    'Element 25 Limited','Global X Ultra Short Nasdaq 100 Hedge Fund','360 Capital REIT','Keypath Education International Inc','Hitech Group Australia Limited',
    'Veem Limited','Airtasker Limited','Environmental Group Limited (the)','Minbos Resources Limited','Betashares India Quality ETF','Credit Clear Limited',
    'MLG OZ Limited','Ishares Global Aggregate Bond Esg (Aud Hedged) ETF','Rumble Resources Limited','Latrobe Magnesium Limited','Namoi Cotton Limited',
    'Diatreme Resources Limited','GTN Limited','RHYTHM Biosciences Limited','Sierra Rutile Holdings Limited','National Tyre & Wheel Limited','Excelsior Capital Limited',
    'Curvebeam Ai Limited','Lepidico Limited','New Zealand Oil & Gas Limited','Acorn Capital Investment Fund Limited','Ryder Capital Limited','Galileo Mining Limited',
    'Betashares Japan ETF-Currency Hedged','Havilah Resources Limited','Vita Life Sciences Limited','Move Logistics Group Limited','Poseidon Nickel Limited',
    'Amaero International Limited','Genmin Limited','Vanguard Ethically Conscious GLB Agg Bond INDEX (Hedged) ETF','Clean Seas Seafood Limited','Ausgold Limited',
    'Cyprium Metals Limited','Orthocell Limited','Medical Developments International Limited','Betashares CRYPTO Innovators ETF','Rand Mining Limited',
    'Mitchell Services Limited','Vysarn Limited','Troy Resources Limited','Pacific Edge Limited','Tigers Realm Coal Limited','FBR Limited','Intelligent Investor Aus Equity Income Fund (Managed Fund)',
    'Astron Corporation Limited','Vaneck Morningstar Australian Moat Income ETF','New World Resources Limited','VHM Limited','Galena Mining Limited','Iron Road Limited',
    'DRA Global Limited',
    'Thorney Technologies Limited',
    'Rectifier Technologies Limited',
    'Joyce Corporation Limited',
    'Tamawood Limited',
    'Wiluna Mining Corporation Limited',
    'Echoiq Limited',
    'Zeotech Limited',
    'Walkabout Resources Limited',
    'Sequoia Financial Group Limited',
    'Clearvue Technologies Limited',
    'Cannindah Resources Limited',
    'Betashares Aust Small Companies Select Fund (Managed Fund)',
    'Adrad Holdings Limited',
    'Microequities Asset Management Group Limited',
    'ROX Resources Limited',
    'Sietel Limited',
    'Montaka GBL Long Only Equities Fund (Managed Fund)',
    'Intelligent Investor Ethical Share Fund (Managed Fund)',
    'Hancock & Gore Limited',
    'KGL Resources Limited',
    'Sunstone Metals Limited',
    'Vaneck Video Gaming and Esports ETF',
    'TMK Energy Limited',
    'Bluglass Limited',
    'S2 Resources Limited',
    'Count Limited',
    'Auteco Minerals Limited',
    'Global X S&P 500 High Yield Low Volatility ETF',
    "Mcpherson's Limited",
    'Advance Zinctek Limited',
    'A-Cap Energy Limited',
    'Chesser Resources Limited',
    'Pointerra Limited',
    'Critical Resources Limited',
    'Besra Gold Inc',
    'Anteotech Limited',
    'Vaneck Global Healthcare Leaders ETF',
    'Ionic Rare EARTHS Limited',
    'Mayfield Childcare Limited',
    'Genetic Signatures Limited',
    'Titan Minerals Limited',
    'Betashares Global Shares ETF',
    'Switzer Dividend Growth Fund (Managed Fund)',
    'Tyranna Resources Limited',
    'Strickland Metals Limited',
    'Global X S&P/ASX 200 High Dividend ETF',
    'Kairos Minerals Limited',
    'Plenti Group Limited',
    'Dusk Group Limited',
    'Dome Gold Mines Limited',
    'Technology Metals Australia Limited',
    'Apiam Animal Health Limited',
    'Investigator Resources Limited',
    'Hartshead Resources NL',
    'Reckon Limited',
    'Micro-X Limited',
    'VRX Silica Limited',
    'Inoviq Limited',
    'Integrated Research Limited',
    'Swoop Holdings Limited',
    'Pental Limited',
    'Somnomed Limited',
    'Betashares Ethical Diversified High Growth ETF',
    'Optiscan Imaging Limited',
    'Ai-Media Technologies Limited',
    'Superior Resources Limited',
    'Global X Ultra Long Nasdaq 100 Hedge Fund',
    'Prescient Therapeutics Limited',
    'Blackstone Minerals Limited',
    'Elixir Energy Limited',
    'Pure Hydrogen Corporation Limited',
    'Ecograf Limited',
    'Peel Mining Limited',
    'Ixup Limited',
    'Lion Selection Group Limited',
    'Tungsten Mining NL',
    'American Rare EARTHS Limited',
    'Asf Group Limited',
    'Brookside Energy Limited',
    'Black Cat Syndicate Limited',
    'MC Mining Limited',
    'Vmoto Limited',
    'Simonds Group Limited',
    'Ecofibre Limited',
    'Lithium Energy Limited',
    'Nova Minerals Limited',
    'Mayur Resources Limited',
    'Neurizer Limited',
    'Mcgrath Limited',
    'Good Drinks Australia Limited',
    'Duxton Farms Limited',
    'Alphinity Global Sustainable Fund (Managed Fund)',
    'CD Private Equity Fund Ii',
    'Po Valley Energy Limited',
    'Canyon Resources Limited',
    'Lakes Blue Energy NL',
    'Nuenergy Gas Limited',
    'Antisense Therapeutics Limited',
    'Agrimin Limited',
    'Global X India Nifty 50 ETF',
    'Lucapa Diamond Company Limited',
    'Orcoda Limited',
    'Schroder Real Return (Managed Fund)',
    'Starpharma Holdings Limited',
    'Focus Minerals Limited',
    'Alliance Nickel Limited',
    'Energy Transition Minerals Limited',
    'Salter Brothers Emerging Companies Limited',
    'TPC Consolidated Limited',
    'Earlypay Limited',
    'Widgie Nickel Limited',
    'Touch Ventures Limited',
    'Pro-Pac Packaging Limited',
    'Betashares MRTN Currie RL Inc Fund (Managed Fund)',
    'Aston Minerals Limited',
    'Beamtree Holdings Limited',
    'Wam Active Limited',
    'Betashares Global Gold Miners ETF - Currency Hedged',
    'Vaneck MSCI Multifactor Em Markets Equity ETF',
    'Aims Property Securities Fund',
    'Moneyme Limited',
    'Meeka Metals Limited',
    'Buru Energy Limited',
    'Wa Kaolin Limited',
    'Ishares Edge MSCI Australia Multifactor ETF',
    'Matrix Composites & Engineering Limited',
    'Ishares Ftse GBL Infrastructure (Aud Hedged) ETF',
    'Calima Energy Limited',
    'Thorn Group Limited',
    'Donaco International Limited',
    'Arizona Lithium Limited',
    'Arovella Therapeutics Limited',
    'Prospa Group Limited',
    'Ellerston Asia Growth Fund (Hedge Fund)',
    'Betashares Cloud Computing ETF',
    'Austral Resources Australia Limited',
    'Midway Limited',
    'Cann Group Limited',
    'Intelligent Monitoring Group Limited',
    'Vital Metals Limited',
    'Morphic Ethical Equities Fund Limited',
    'Noble Helium Limited',
    'Auctus Investment Group Limited',
    'Kingsrose Mining Limited',
    'Ironbark Capital Limited',
    'Loyal Lithium Limited',
    'CYGNUS Metals Limited',
    'Little Green Pharma Limited',
    'Scidev Limited',
    'Eumundi Group Limited',
    'True North Copper Limited',
    'Betashares Managed Risk Global Share Fund (Managed Fund)',
    'Centrepoint Alliance Limited',
    'Boom Logistics Limited',
    'Gale Pacific Limited',
    'Naos Emerging Opportunities Company Limited',
    'Universal Biosensors Inc',
    'Kalium Lakes Limited',
    'Betashares Australian Equities Bear (Hedge Fund)',
    'Future Battery Minerals Limited',
    'US Student Housing REIT',
    'Astral Resources NL',
    'Vaneck Small Companies Masters ETF',
    'Icandy Interactive Limited',
    'Hammer Metals Limited',
    'Tombador Iron Limited',
    'Ishares J.P. Morgan Usd Emerging Markets (Aud Hedged) ETF',
    'Austco Healthcare Limited',
    'Maggie Beer Holdings Limited',
    'Raiden Resources Limited',
    'Global X Hydrogen ETF',
    'Russell Investments Australian Semi-Government Bond ETF',
    'Lumos Diagnostics Holdings Limited',
    'Aspire Mining Limited',
    'Terramin Australia Limited',
    'Euro Manganese Inc',
    'AVA Risk Group Limited',
    'Province Resources Limited',
    'Sports Entertainment Group Limited',
    'Prime Financial Group Limited',
    'Bluebet Holdings Limited',
    'Avada Group Limited',
    'Toro Energy Limited',
    'Renergen Limited',
    'Teaminvest Private Group Limited',
    'BNK Banking Corporation Limited',
    'Centrex Limited',
    'Southern Cross Gold Limited',
    'Advanced Health Intelligence Limited',
    'Antipa Minerals Limited',
    'RAIZ Invest Limited',
    'Wide Open Agriculture Limited',
    'Wisr Limited SPONSORED',
    'KIN Mining NL',
    'Artemis Resources Limited',
    'Actinogen Medical Limited',
    'Openpay Group Limited',
    'CUE Energy Resources Limited',
    'Eildon Capital Group',
    'Betashares Global Quality Leaders ETF Currency Hedged',
    'Lithium Australia Limited',
    'Australian Pacific Coal Limited',
    'Elsight Limited',
    'Vection Technologies Limited',
    'First Graphene Limited',
    'Prospect Resources Limited',
    'Betashares Europe ETF-Currency Hedged',
    'Tanami Gold NL',
    'Flagship Investments Limited',
    'BENZ Mining Corp',
    'SPDR MSCI World Quality MIX Fund',
    'Alternative Investment Trust',
    'Nico Resources Limited',
    'Neurotech International Limited',
    'FFI Holdings Limited',
    'Betashares Global Banks ETF - Currency Hedged',
    'Far East Gold Limited',
    'Harmoney Corp Limited',
    'Top Shelf International Holdings Limited',
    'Lowell Resources Fund',
    'Betashares Global Uranium ETF',
    'Straker Limited',
    'Prophecy International Holdings Limited',
    'Whispir Limited',
    'Zenith Minerals Limited',
    'RTG Mining Inc',
    'Metarock Group Limited',
    'Betashares Australian Financials Sector ETF',
    'Barton Gold Holdings Limited',
    'Loomis Sayles GBL EQ Fund (Quoted Managed Fund)',
    'SPDR S&P/ASX 200 Esg Fund',
    'Perennial Better Future Fund (Managed Fund)',
    'Polymetals Resources Limited',
    'Magontec Limited',
    'BSA Limited',
    'Triton Minerals Limited',
    'Horizon Gold Limited',
    'Pan Asia Metals Limited',
    'Blue Star Helium Limited',
    'Strategic Elements Limited',
    'Dubber Corporation Limited',
    'Veris Limited',
    'Novatti Group Limited',
    'Redflow Limited',
    'Kinatico Limited',
    'Metalstech Limited SPONSORED',
    'Adacel Technologies Limited',
    'Noumi Limited',
    'Central Petroleum Limited',
    'Dynamic Group Holdings Limited',
    'BWX Limited',
    'Naos Ex-50 Opportunities Company Limited',
    'Argenica Therapeutics Limited',
    'Kingston Resources Limited',
    'Infinity Lithium Corporation Limited',
    'Desane Group Holdings Limited',
    'Cirrus Networks Holdings Limited',
    'Sovereign Cloud Holdings Limited',
    'Pacific Nickel Mines Limited SPONSORED',
    'Li-S Energy Limited',
    'Painchek Limited',
    'Impact Minerals Limited SPONSORED',
    'Invion Limited',
    'Hawthorn Resources Limited',
    'Mayfield Group Holdings Limited',
    'Change Financial Limited',
    'Mustera Property Group Limited',
    'De.Mem Limited',
    'FAR Limited',
    'Reach Resources Limited',
    'Webcentral Limited',
    'Red River Resources Limited',
    'Income Asset Management Group Limited',
    'Global X S&P Biotech ETF',
    'Selfwealth Limited',
    'Vanadium Resources Limited',
    'State GAS Limited',
    'Etherstack Plc',
    'Ora Gold Limited',
    'Katana Capital Limited',
    'Ras Technology Holdings Limited',
    'Nova EYE Medical Limited',
    'Carbon Revolution Limited',
    'Blackwall Limited',
    'REY Resources Limited',
    'SPDR S&P/ASX Australian Bond Fund',
    'Australian Rare EARTHS Limited',
    'Betashares Ethical Diversified Growth ETF',
    'Vintage Energy Limited',
    'KAZIA Therapeutics Limited',
    'Duketon Mining Limited',
    'Morella Corporation Limited',
    'CZR Resources Limited',
    'Macarthur Minerals Limited',
    'Emmerson Resources Limited',
    'Volt Resources Limited',
    'Compumedics Limited',
    'Vaneck Morningstar International Wide Moat ETF',
    'Xref Limited',
    'Great Boulder Resources Limited',
    'Warriedar Resources Limited',
    'Montaka Global Extension Fund (Quoted Managed Hedge Fund)',
    'Jade Gas Holdings Limited',
    'Firebrick Pharma Limited',
    'Rma Global Limited',
    'Xtek Limited',
    'Aerometrex Limited',
    'Alto Metals Limited',
    'West Wits Mining Limited',
    'Clime Capital Limited',
    'Sensen Networks Limited',
    'Pioneer Credit Limited',
    'Provaris Energy Limited',
    'Nuheara Limited',
    'Kip Mcgrath Education Centres Limited',
    'Greenvale Energy Limited',
    'Richmond Vanadium Technology Limited',
    'Pureprofile Limited',
    'Mineral Commodities Limited',
    'Pilot Energy Limited',
    'Lefroy Exploration Limited',
    'Diverger Limited',
    'Urbanise.com Limited',
    'Kuniko Limited',
    'Marley Spoon Se',
    'Tombola Gold Limited',
    'Mad Paws Holdings Limited',
    'Foresta Group Holdings Limited',
    'ST George Mining Limited',
    '92 Energy Limited',
    'Einvest Income Generator Fund (Managed Fund)',
    'Marmota Limited',
    'Retech Technology Co. Limited',
    'ADX Energy Limited',
    'Soco Corporation Limited',
    'Aerison Group Limited',
    'Vaneck Bentham GL Cap Se Active ETF (Managed Fund)',
    'Indiana Resources Limited',
    'Trek Metals Limited',
    'Falcon Metals Limited',
    'Omega Oil & Gas Limited',
    'Academies Australasia Group Limited',
    'QEM Limited',
    'Netlinkz Limited',
    'Tlou Energy Limited',
    'Cryosite Limited',
    'Blue Energy Limited',
    'Global Masters Fund Limited',
    'Boab Metals Limited',
    'Munro Climate Change Leaders Fund (Managed Fund)',
    'DGR Global Limited',
    'WIA Gold Limited',
    'Mosaic Brands Limited',
    'SPDR S&P/ASX Australian Government Bond Fund',
    'Butn Limited',
    'Unico Silver Limited',
    'Pharmaxis Limited',
    'Bass Oil Limited',
    'GWR Group Limited',
    'WRKR Limited',
    'Eagle Mountain Mining Limited',
    'Hawsons Iron Limited',
    'Triangle Energy (Global) Limited',
    'Secos Group Limited',
    'Respiri Limited',
    'Evolution Energy Minerals Limited',
    'Archtis Limited',
    'Field Solutions Holdings Limited',
    'Stavely Minerals Limited',
    'Pursuit Minerals Limited',
    'News Corporation',
    'Aspermont Limited',
    'Pentanet Limited',
    'Adveritas Limited',
    'Parkway Corporate Limited',
    'Clime Investment Management Limited',
    'WT Financial Group Limited',
    'Strata Investment Holdings Plc',
    'Western Mines Group Limited',
    'Spirit Technology Solutions Limited',
    'Manuka Resources Limited',
    'Turaco Gold Limited',
    'Comms Group Limited',
    'Horizon Minerals Limited',
    'Navarre Minerals Limited',
    'Magnetite Mines Limited',
    'Eclipse Metals Limited',
    'Damstra Holdings Limited',
    'Digitalx Limited',
    'CD Private Equity Fund I',
    'Ecargo Holdings Limited',
    'Red Metal Limited',
    'Cadence Opportunities Fund Limited',
    'Senetas Corporation Limited',
    'Alloggio Group Limited',
    'Altamin Limited',
    'Industrial Minerals Limited',
    'Betashares Global Income Leaders ETF',
    'Greenwing Resources Limited',
    'NGE Capital Limited',
    'Jatcorp Limited',
    'Dimerix Limited',
    'Betashares Managed Risk AUS SH Fund (Managed Fund)',
    'Alara Resources Limited',
    'Resource Mining Corporation Limited',
    'Elementos Limited',
    'Energy Metals Limited',
    'Pharmaust Limited',
    'Vaneck 1-3 Month US Treasury Bond ETF',
    'Solis Minerals Limited',
    'SPDR S&P/ASX Small Ordinaries Fund',
    'Carnavale Resources Limited',
    'Bioxyne Limited',
    'Kaiser Reef Limited',
    'Carawine Resources Limited',
    'Red Sky Energy Limited',
    'Australis Oil & Gas Limited',
    'Daintree HYBRID Opportunities Fund (Managed Fund)',
    'Manhattan Corporation Limited',
    'Talisman Mining Limited',
    'Ioupay Limited',
    'Harvest Technology Group Limited',
    'Coda Minerals Limited',
    'Corum Group Limited',
    'LCL Resources Limited',
    'Intell Invest Select Value SHR Fund (Managed Fund)',
    'Imexhs Limited',
    'Biotron Limited',
    'Atomos Limited',
    'Decmil Group Limited',
    'EZZ Life Science Holdings Limited',
    'RAREX Limited',
    'Birddog Technology Limited',
    'Saturn Metals Limited',
    'Spenda Limited',
    'Buxton Resources Limited',
    'The Original Juice Co. Limited',
    'Glennon Small Companies Limited',
    'Venture Minerals Limited',
    'Resonance Health Limited',
    'FYI Resources Limited',
    'Cluey Limited',
    'Amani Gold Limited',
    'Talius Group Limited',
    'QX Resources Limited',
    'H&G High Conviction Limited',
    'Metro Performance Glass Limited',
    'Metallica Minerals Limited',
    'Decmil Group Limited',
    'Battery Age Minerals Limited SPONSORED',
    'EDU Holdings Limited',
    'Surefire Resources NL',
    'Celsius Resources Limited',
    'Emyria Limited',
    'Hannans Limited',
    'South HARZ Potash Limited',
    'Jayride Group Limited',
    'Sihayo Gold Limited',
    'Verbrec Limited',
    'ECS Botanics Holdings Limited',
    'Belararox Limited',
    'Whitefield Industrials Limited',
    'Seafarms Group Limited',
    'Advanced Share Registry Limited',
    'RPM Automotive Group Limited',
    'ANAX Metals Limited',
    'Wellard Limited',
    'Alicanto Minerals Limited',
    'Ensurance Limited',
    'Tian An Australia Limited',
    'Venus Metals Corporation Limited',
    'Fat Prophets Global Contrarian Fund Limited',
    'Nexus Minerals Limited',
    'Unith Limited',
    'Medallion Metals Limited',
    'Cynata Therapeutics Limited',
    'Weststar Industrial Limited',
    'Splitit Payments Limited',
    'Fertoz Limited',
    'Jaxsta Limited',
    'Cleanspace Holdings Limited',
    'Metals Australia Limited',
    'Genetic Technologies Limited',
    'Galilee Energy Limited',
    'Transmetro Corporation Limited',
    'Wellnex Life Limited',
    'Living Cell Technologies Limited',
    'IDT Australia Limited',
    'Booktopia Group Limited',
    'Betashares MRTN Currie EQY Inc Fund (Managed Fund)',
    'Mandrake Resources Limited',
    'Radiopharm Theranostics Limited',
    'Suvo Strategic Minerals Limited',
    'Betashares Energy Transition Metals ETF',
    'Embelton Limited',
    'Adherium Limited',
    'Jupiter Energy Limited',
    'ABX Group Limited',
    'Tennant Minerals Limited',
    'AML3D Limited',
    'Greentech Metals Limited',
    'Connexion Telematics Limited',
    'Oncosil Medical Limited',
    'Magnum Mining and Exploration Limited',
    'Equatorial Resources Limited',
    'Heramed Limited',
    '360 Capital Mortgage REIT',
    'Betashares Ethical Diversified Balanced ETF',
    'Ishares Yield Plus ETF',
    'Rhinomed Limited',
    'Clean TEQ Water Limited',
    'Bcal Diagnostics Limited',
    'Vectus Biosystems Limited',
    'Biome Australia Limited',
    'Recharge Metals Limited',
    'Buddy Technologies Limited',
    'Tesoro Gold Limited',
    'Cardiex Limited',
    'ARTRYA Limited',
    'Brightstar Resources Limited',
    'Copper Strike Limited',
    'Naos Emerging Opportunities Company Limited',
    'Australian Silica Quartz Group Limited',
    'A1 Investments & Resources Limited',
    'Beam Communications Holdings Limited',
    'Melodiol Global Health Limited',
    'Ambertech Limited',
    'Activeport Group Limited',
    'Jameson Resources Limited',
    'Itech Minerals Limited',
    'Nagambie Resources Limited',
    'Globe Metals & Mining Limited',
    'Quickstep Holdings Limited',
    'Xreality Group Limited',
    'Chimeric Therapeutics Limited',
    'Imagion Biosystems Limited',
    'Alterity Therapeutics Limited',
    'Shekel Brainweigh Limited',
    'Cobre Limited',
    'Phosco Limited',
    'Okapi Resources Limited',
    'Vaneck Ftse China A50 ETF',
    'Scorpion Minerals Limited',
    'Gold Mountain Limited',
    'Carbonxt Group Limited',
    'SPDR S&P Emerging Markets Carbon Control Fund',
    'Cosmos Exploration Limited',
    'SKY Metals Limited',
    'Kleos Space S.A',
    'Future Metals NL',
    'ECP Emerging Growth Limited',
    'Flagship Investments Limited',
    'Findi Limited',
    'Apollo Minerals Limited',
    'Livehire Limited',
    'Parabellum Resources Limited',
    'Sarytogan Graphite Limited',
    'Sparc Technologies Limited',
    'Atlas Pearls Limited',
    'Betashares Australian Quality ETF',
    'Complii Fintech Solutions Limited',
    'Magmatic Resources Limited',
    'Aeon Metals Limited',
    'PATRYS Limited',
    'SKYFII Limited',
    'BBX Minerals Limited',
    'Ishares Edge MSCI Australia Minimum Volatility ETF',
    'Investsmart Group Limited',
    'Peppermint Innovation Limited',
    'Lithium Universe Limited SPONSORED',
    'Frugl Group Limited',
    'Yojee Limited',
    'Midas Minerals Limited',
    'K2 Asset Management Holdings Limited',
    'Platina Resources Limited',
    'Maronan Metals Limited',
    'Immuron Limited',
    'Everest Metals Corporation Limited',
    'Yellow Brick Road Holdings Limited',
    'Power Minerals Limited',
    'Iceni Gold Limited',
    'Monash Investors SML Companies Trust (Hedge Fund)',
    'Qmines Limited',
    'ENTYR Limited',
    'Titomic Limited',
    'Axiom Properties Limited',
    'Victor Group Holdings Limited',
    'Kalamazoo Resources Limited',
    'Auscann Group Holdings Limited',
    'Odyssey Gold Limited',
    'Doctor Care Anywhere Group Plc',
    'Xantippe Resources Limited',
    'White Rock Minerals Limited',
    'Tambourah Metals Limited',
    'Matador Mining Limited',
    'Askari Metals Limited',
    'Avenira Limited',
    'Farm Pride Foods Limited',
    'Atomo Diagnostics Limited',
    'Golden Rim Resources Limited',
    'Akora Resources Limited',
    'Environmental Clean Technologies Limited',
    'Amplia Therapeutics Limited',
    '8COMMON Limited',
    'Cazaly Resources Limited',
    'Millennium Services Group Limited',
    'Caspin Resources Limited',
    'Aldoro Resources Limited',
    'Lanthanein Resources Limited',
    'BPH Energy Limited',
    'Victory Metals Limited',
    'Pacgold Limited',
    'Orbital Corporation Limited',
    'SKS Technologies Group Limited',
    'Naos Ex-50 Opportunities Company Limited',
    'Cassius Mining Limited',
    'Orion Metals Limited',
    'Sabre Resources Limited',
    'EVZ Limited',
    'Peregrine Gold Limited',
    'Viridis Mining and Minerals Limited',
    'Lithium Plus Minerals Limited',
    'Sunshine Metals Limited',
    'Bulletin Resources Limited',
    'PNX Metals Limited',
    'Ardiden Limited',
    'Vanguard Global Minimum Volatility Active ETF (Managed Fund)',
    'NSX Limited',
    'Nuchev Limited',
    'Beston Global Food Company Limited',
    'K2FLY Limited',
    'Bio-Gene Technology Limited',
    'Antilles Gold Limited',
    'Grand Gulf Energy Limited',
    'Vaneck Gold Bullion ETF',
    'Strike Resources Limited',
    'Astute Metals NL',
    'N1 Holdings Limited',
    'OAR Resources Limited',
    'Apostle Dundas Global Equity Classd (Managed Fund)',
    'Fitzroy River Corporation Limited',
    'Carnegie Clean Energy Limited',
    'Phoslock Environmental Technologies Limited',
    'Lion One Metals Limited',
    'Geopacific Resources Limited',
    'Gti Energy Limited',
    'Beforepay Group Limited',
    'International Graphite Limited',
    'Mount Ridley Mines Limited',
    'King River Resources Limited',
    'London City Equities Limited',
    'Althea Group Holdings Limited',
    'Fat Prophets Global Property Fund',
    'Valor Resources Limited',
    'Flexiroam Limited',
    'Minrex Resources Limited',
    'Kalina Power Limited',
    'Avecho Biotechnology Limited',
    'AJ Lucas Group Limited',
    'Almonty Industries Inc',
    'Gold Hydrogen Limited',
    'Medlab Clinical Limited',
    'East 33 Limited',
    'Dateline Resources Limited SPONSORED',
    'Odin Metals Limited',
    'EV Resources Limited',
    'NGX Limited',
    'Sportshero Limited',
    'Af Legal Group Limited',
    'Cleo Diagnostics Limited',
    'Voltaic Strategic Resources Limited',
    'Acumentis Group Limited',
    'Revasum Inc',
    'Advanced Braking Technology Limited',
    'Greenstone Resources Limited',
    'Rimfire Pacific Mining Limited',
    'Vaneck Global Listed Private Equity ETF',
    'Burley Minerals Limited',
    'Podium Minerals Limited',
    'High Peak Royalties Limited',
    'Asian American Medical Group Limited',
    'Jpmorgan EQ Prem Income Active ETF (Managed Fund)',
    'Castile Resources Limited',
    'Augustus Minerals Limited',
    'Norwood Systems Limited',
    'Quickfee Limited',
    'Aquirian Limited',
    'Baumart Holdings Limited',
    'FELIX Group Holdings Limited',
    'Corella Resources Limited',
    'Lode Resources Limited',
    'Riedel Resources Limited',
    'Mont Royal Resources Limited',
    'Finexia Financial Group Limited',
    'Citigold Corporation Limited',
    '3D Oil Limited',
    'Great Southern Mining Limited',
    'Paterson Resources Limited',
    'INVEX Therapeutics Limited',
    'Bluechiip Limited',
    'Savannah Goldfields Limited',
    'Evergreen Lithium Limited',
    'Energy Technologies Limited',
    'Fatfish Group Limited',
    'Alchemy Resources Limited',
    'Hamelin Gold Limited',
    'Revolver Resources Holdings Limited',
    'Incentiapay Limited',
    'ACRUX Limited',
    'Oceana Lithium Limited SPONSORED',
    'Papyrus Australia Limited',
    'Renu Energy Limited',
    'Resource Base Limited',
    'Betashares Electric Vehicles and FTR Mobility ETF',
    'Matsa Resources Limited',
    'Metal Bank Limited',
    'Austral Gold Limited',
    'Polarx Limited',
    'Memphasys Limited',
    'Charger Metals NL',
    'The Agency Group Australia Limited',
    'Toubani Resources Inc',
    'Mobilicom Limited',
    'Mako Gold Limited',
    'BIR Financial Limited',
    'Rewardle Holdings Limited',
    'Adslot Limited',
    'Allegiance Coal Limited',
    'Petratherm Limited',
    'Neuroscientific Biopharmaceuticals Limited',
    'Lodestar Minerals Limited',
    'Argent Minerals Limited',
    'Stealth Global Holdings Limited',
    'Cufe Limited',
    'Cardno Limited',
    'Armour Energy Limited',
    'Perpetual Resources Limited',
    'Star Combo Pharma Limited',
    'Halo Technologies Holdings Limited',
    '1ST Group Limited',
    'Gold 50 Limited',
    'Copper Search Limited',
    'Global X Metal Securities Australia Limited',
    'Alvo Minerals Limited',
    'Tissue Repair Limited',
    'Pure Foods Tasmania Limited',
    'Ishares Ftse GBL Property Ex Aus (Aud Hedged) ETF',
    'Nordic Nickel Limited',
    'Solstice Minerals Limited',
    'Torque Metals Limited',
    'Southern Palladium Limited',
    'Zelira Therapeutics Limited',
    'Jcurve Solutions Limited',
    'Siren Gold Limited',
    'EQUUS Mining Limited',
    'Platinum Transition (Quoted Managed Hedge Fund)',
    'Betashares Strong Australian Dollar Fund (Hedge Fund)',
    'Mosaic Brands Limited',
    'Stelar Metals Limited',
    'GBM Resources Limited',
    'Hills Limited',
    'Credit Intelligence Limited',
    'Leeuwin Metals Limited',
    'Ballymore Resources Limited',
    'Firetail Resources Limited',
    'Eden Innovations Limited',
    'Patriot Lithium Limited',
    'RLF Agtech Limited',
    'Hudson Investment Group Limited',
    'Lachlan Star Limited',
    'Estrella Resources Limited',
    'Castle Minerals Limited',
    'Tasfoods Limited',
    'HEJAZ Property Fund (Managed Fund)',
    'Livetiles Limited',
    'Evion Group NL',
    'Ironbark ZINC Limited',
    'Rare Foods Australia Limited',
    'Megado Minerals Limited',
    'Metgasco Limited',
    'MGC Pharmaceuticals Limited',
    'Xamble Group Limited',
    'AXP Energy Limited',
    'HELIX Resources Limited',
    'Asra Minerals Limited',
    'Woomera Mining Limited',
    'Riversgold Limited',
    'Hubify Limited',
    'BOD Science Limited',
    'ZICOM Group Limited',
    'Kingfisher Mining Limited',
    'Many Peaks Gold Limited',
    'Eastern Resources Limited',
    'Openn Negotiation Limited',
    'Vaughan Nelson Global Smid Fund (Managed Fund)',
    'Australian Dairy Nutritionals Limited',
    'Hygrovest Limited',
    'Equity Trustees Limited',
    'OD6 Metals Limited',
    'Alma Metals Limited',
    'Associate Global Partners Limited',
    'Krakatoa Resources Limited',
    'Hyterra Limited',
    'SI6 Metals Limited',
    'Stonehorse Energy Limited',
    'Gratifii Limited',
    'Sensore Limited',
    'Design Milk Co Limited',
    'Infinity Mining Limited',
    'Firetrail S3 Global Opps Fund (Managed Fund)',
    'Osteopore Limited',
    'Aurora Energy Metals Limited',
    'Gullewa Limited',
    'Volt Power Group Limited',
    'Reward Minerals Limited',
    'Great Western Exploration Limited',
    'Marquee Resources Limited',
    'Golden Mile Resources Limited',
    'Noxopharm Limited',
    'Prodigy Gold NL',
    'Land & Homes Group Limited',
    'VONEX Limited',
    'Tinybeans Group Limited',
    'Whitehawk Limited',
    'Australian Mines Limited',
    'Nimy Resources Limited',
    'One Click Group Limited',
    'Ragnar Metals Limited',
    'Fintech Chain Limited',
    'Balkan Mining and Minerals Limited',
    'Koba Resources Limited',
    'Rent.com.Au Limited',
    'Cyclone Metals Limited',
    'Mighty Craft Limited',
    'Yari Minerals Limited',
    'Red Mountain Mining Limited',
    'Norwest Minerals Limited',
    'Stellar Resources Limited',
    'White Cliff Minerals Limited',
    'Arcadia Minerals Limited',
    'Southern Hemisphere Mining Limited',
    'GLG Corp Limited',
    'Auking Mining Limited',
    'Truscreen Group Limited',
    'ECP Emerging Growth Limited',
    'Betashares British Pound ETF',
    'Enegex Limited',
    'Uscom Limited',
    'Ausquest Limited',
    'Lion Energy Limited',
    'Babylon Pump & Power Limited',
    'Ep&T Global Limited',
    'Pivotal Metals Limited',
    'Alexium International Group Limited',
    'Larvotto Resources Limited',
    'Keybridge Capital Limited',
    'Intra Energy Corporation Limited',
    'Kingsland Global Limited',
    'Olympio Metals Limited',
    'Adalta Limited',
    'Errawarra Resources Limited',
    'Adavale Resources Limited',
    'Classic Minerals Limited',
    'Bounty Oil & Gas NL',
    'Mitre Mining Corporation Limited',
    'Bikeexchange Limited',
    'Betashares Strong U.S. Dollar Fund (Hedge Fund)',
    'Marvel Gold Limited',
    'Firebird Metals Limited',
    'Juno Minerals Limited',
    'Cape Range Limited',
    'Yandal Resources Limited',
    'Javelin Minerals Limited',
    'Metal Hawk Limited',
    'Conico Limited',
    'Aoris Int Fund (Class D) (Hedged) (Managed Fund)',
    'Global Masters Fund Limited',
    'Austchina Holdings Limited',
    'Lycaon Resources Limited',
    'Gateway Mining Limited',
    'Taiton Resources Limited',
    'Newpeak Metals Limited',
    'Viking Mines Limited',
    'Inca Minerals Limited',
    'Medibio Limited',
    'Site Group International Limited',
    'Streamplay Studio Limited',
    'Castillo Copper Limited',
    'Traffic Technologies Limited',
    'Nanoveu Limited',
    'Arrow Minerals Limited',
    '1414 Degrees Limited',
    'RUBIX Resources Limited',
    'Ark Mines Limited',
    'CPT Global Limited',
    'Swift Networks Group Limited',
    'SIV Capital Limited',
    'Resources & Energy Group Limited',
    'Maximus Resources Limited',
    'ZOOM2U Technologies Limited',
    'Green Critical Minerals Limited',
    'FELIX Gold Limited',
    'FLYNN Gold Limited',
    'Equity Trustees Limited',
    'Equity Trustees Limited',
    'Xpon Technologies Group Limited',
    'Domacom Limited',
    'Roolife Group Limited',
    'Knosys Limited',
    'Nanollose Limited',
    'Motio Limited',
    'Corazon Mining Limited',
    'CAQ Holdings Limited',
    'Thrive Tribe Technologies Limited',
    'Renegade Exploration Limited',
    'Broo Limited',
    'Athena Resources Limited',
    'Titanium Sands Limited',
    'Equity Trustees Limited',
    'Inhalerx Limited',
    'Lincoln Minerals Limited',
    'DTI Group Limited',
    'Australian Critical Minerals Limited',
    'Linius Technologies Limited',
    'Innlanz Limited',
    'K2 Australian Small Cap Fund (Hedge Fund)',
    'New Talisman Gold Mines Limited',
    'Wiseway Group Limited',
    'GCX Metals Limited',
    'Australasian Metals Limited',
    'Black Canyon Limited',
    'Gladiator Resources Limited',
    'Live Verdure Limited',
    'Aguia Resources Limited',
    'Equity Trustees Limited',
    '8I Holdings Limited',
    'Schrole Group Limited',
    'Moab Minerals Limited',
    'BLAZE Minerals Limited',
    'ZOONO Group Limited',
    'Way 2 Vat Limited',
    'Iltani Resources Limited',
    'Global Health Limited',
    'Spacetalk Limited',
    'FOS Capital Limited',
    'Kore Potash Plc',
    'X2M Connect Limited',
    'Locality Planning Energy Holdings Limited',
    'Oldfields Holdings Limited',
    'Icetana Limited',
    'Accelerate Resources Limited',
    'African Gold Limited',
    'Critical Minerals Group Limited',
    'HYDRIX Limited',
    'PVW Resources Limited',
    'Dynamic Metals Limited',
    'SRJ Technologies Group Plc',
    'Admiralty Resources NL',
    'Truscott Mining Corporation Limited',
    'Southern Gold Limited',
    'Horseshoe Metals Limited',
    'Freehill Mining Limited',
    'Ragusa Minerals Limited',
    'Cradle Resources Limited',
    'Control Bionics Limited',
    'Battery Minerals Limited',
    'Aruma Resources Limited',
    'Emetals Limited',
    'Great Divide Mining Limited',
    'Audalia Resources Limited',
    'Kingsland Minerals Limited',
    'Betashares Interest Rate Hedged Aus Corp Bond ETF',
    'Odessa Minerals Limited',
    'Chilwa Minerals Limited',
    'Legacy Minerals Holdings Limited',
    'Metalicity Limited',
    'Western Yilgarn NL',
    'Coppermoly Limited',
    'Native Mineral Resources Holdings Limited',
    "Toys'R'US ANZ Limited",
    'Korab Resources Limited',
    'Whitebark Energy Limited',
    'Argonaut Resources NL',
    'Pure Resources Limited',
    'Readcloud Limited',
    'R3D Resources Limited',
    'Ookami Limited',
    'Golden Deeps Limited',
    'Terra Uranium Limited',
    'ARC Funds Limited',
    'The Hydration Pharmaceuticals Company Limited',
    'North Stawell Minerals Limited',
    'New Age Exploration Limited',
    'Todd River Resources Limited',
    'Ignite Limited',
    'Aeeris Limited',
    'Top End Energy Limited',
    'Labyrinth Resources Limited',
    'Locksley Resources Limited',
    'Taruga Minerals Limited',
    "Oliver's Real Food Limited",
    'Global Oil & Gas Limited',
    'Constellation Resources Limited',
    'Visioneering Technologies Inc',
    'M3 Mining Limited',
    'AQUIS Entertainment Limited',
    'Atrum Coal Limited',
    'Cipherpoint Limited',
    'Anagenics Limited',
    'DY6 Metals Limited',
    'Purifloh Limited',
    'VDM Group Limited',
    'Aeris Environmental Limited',
    'Betashares Euro ETF',
    'Elixinol Wellness Limited',
    'Patagonia Lithium Limited',
    'Wingara AG Limited',
    'FIN Resources Limited',
    'Zuleika Gold Limited',
    'Sprintex Limited',
    'Aurumin Limited',
    'Bellavista Resources Limited',
    'Equity Trustees Limited',
    'Miramar Resources Limited',
    'Aumake Limited',
    'Botala Energy Limited',
    'West Cobar Metals Limited',
    'LBT Innovations Limited',
    'Tempest Minerals Limited',
    'Cohiba Minerals Limited',
    'Victory Offices Limited',
    'Dominion Minerals Limited',
    'Doriemus Plc',
    'Epsilon Healthcare Limited',
    'Haranga Resources Limited',
    'Discovex Resources Limited',
    'Basin Energy Limited',
    'Kincora Copper Limited',
    'Global X Metal Securities Australia Limited',
    'Yowie Group Limited',
    'Vertex Minerals Limited',
    'Mpower Group Limited',
    'Terrain Minerals Limited',
    'Golden State Mining Limited',
    'Hydrocarbon Dynamics Limited',
    'Lightning Minerals Limited',
    'Future First Technologies Limited',
    'ZEUS Resources Limited',
    'Rocketdna Limited',
    'NT Minerals Limited',
    'Omnia Metals Group Limited',
    'Singular Health Group Limited',
    'Gibb River Diamonds Limited',
    'Kula Gold Limited',
    'Douugh Limited',
    'Island Pharmaceuticals Limited',
    'BMG Resources Limited',
    'Equinox Resources Limited',
    'OZZ Resources Limited',
    'Allegra Orthopaedics Limited',
    'Delorean Corporation Limited',
    'My Rewards International Limited',
    'White Energy Company Limited',
    'Sensera Limited',
    'Catalina Resources Limited',
    'TZ Limited',
    'Openlearning Limited',
    'Cooper Metals Limited',
    'Auric Mining Limited',
    'Mantle Minerals Limited',
    'Codrus Minerals Limited',
    'Dorsavi Limited',
    'Imperial Pacific Limited',
    'Austin Metals Limited',
    'The GO2 People Limited',
    'Enrg Elements Limited',
    'Noronex Limited',
    'Black Dragon Gold Corp',
    'Orexplore Technologies Limited',
    'Vaneck Global Carbon Credits ETF (Synthetic)',
    'Macro Metals Limited',
    'Equity Trustees Limited',
    'Jpmorgan GL Res En in EQ Active ETF (Managed Fund)',
    'Bryah Resources Limited',
    'Prospech Limited',
    'Tempus Resources Limited',
    'BTC Health Limited',
    'Carly Holdings Limited',
    'Nickelx Limited',
    'Energy Action Limited',
    'Ultima United Limited',
    'Discovery Alaska Limited',
    'SSH Group Limited',
    'Carbon Minerals Limited',
    'Rightcrowd Limited',
    'Forrestania Resources Limited',
    'AD1 Holdings Limited',
    'Audeara Limited',
    'Tek-Ocean Group Limited',
    'Connected Io Limited',
    'Cauldron Energy Limited',
    'BPM Minerals Limited',
    'NEX Metals Exploration Limited',
    'Range International Limited',
    'Empire Resources Limited',
    'Powerhouse Ventures Limited',
    'Careteq Limited',
    'Finder Energy Holdings Limited',
    'Global X Usd High Yield Bond ETF(Currency Hedged)',
    'Glennon Small Companies Limited',
    'Australia United Mining Limited',
    'Magnetic Resources NL',
    'Australian Gold and Copper Limited',
    'Australian Agricultural Projects Limited',
    'GREENHY2 Limited',
    'Cann Global Limited',
    'GPS Alliance Holdings Limited',
    'Terragen Holdings Limited',
    'Ozaurum Resources Limited',
    'Desoto Resources Limited',
    'ZINC of Ireland NL',
    'CHEMX Materials Limited',
    'EVE Health Group Limited',
    'Pantera Minerals Limited',
    'Equity Trustees Limited',
    'Redstone Resources Limited',
    'Mighty Kingdom Limited',
    'Protean Energy Limited',
    'Australian Potash Limited',
    'Spectur Limited',
    'Eneco Refresh Limited',
    'Dart Mining NL',
    'Osmond Resources Limited',
    'Health and Plant Protein Group Limited',
    'Equity Trustees Limited',
    'Hexagon Energy Materials Limited',
    'Nightingale Intelligent Systems Inc',
    'IPB Petroleum Limited',
    'Scout Security Limited',
    'Benjamin Hornigold Limited',
    'HITIQ Limited',
    'Adelong Gold Limited',
    'Aoris Int Fund (Class B) (Unhedged) (Managed Fund)',
    'Mithril Resources Limited',
    'Cullen Resources Limited',
    '8VI Holdings Limited',
    'Resolution Minerals Limited',
    'Albion Resources Limited',
    'Caprice Resources Limited',
    'Sipa Resources Limited',
    'Variscan Mines Limited',
    'Tasman Resources Limited',
    'Godolphin Resources Limited',
    'Alderan Resources Limited',
    'Alterra Limited',
    'Coolabah Metals Limited',
    'MTM Critical Metals Limited',
    'High-Tech Metals Limited',
    'Hiremii Limited',
    'Ronin Resources Limited',
    'Narryer Metals Limited',
    'Bindi Metals Limited',
    'Auris Minerals Limited',
    'Saferoads Holdings Limited',
    'Aurora Labs Limited',
    'Heavy Minerals Limited',
    'Analytica Limited',
    'Pivotal Systems Corporation',
    'Clara Resources Australia Limited',
    'Kneomedia Limited',
    'Opyl Limited',
    'Strategic Energy Resources Limited',
    'M8 Sustainable Limited',
    'Constellation Technologies Limited',
    'MRG Metals Limited',
    'Lykos Metals Limited',
    'MCS Services Limited',
    'International Equities Corporation Limited',
    'Traka Resources Limited',
    'First Au Limited',
    'Thomson Resources Limited',
    'Bastion Minerals Limited',
    'Summit Minerals Limited',
    'Nelson Resources Limited',
    'Norfolk Metals Limited',
    'E79 Gold Mines Limited',
    'Datadot Technology Limited',
    'Elmore Limited',
    'Kalgoorlie Gold Mining Limited',
    'Bubalus Resources Limited',
    'Equity Trustees Limited',
    'Metalsgrove Mining Limited',
    'Koonenberry Gold Limited',
    'The Calmer Co International Limited',
    'GAS2GRID Limited',
    'Nyrada Inc',
    'Love Group Global Limited',
    'Canterbury Resources Limited',
    'RBR Group Limited',
    'Black Mountain Energy Limited',
    'Betashares Global Shares ETF - Currency Hedged',
    'Sultan Resources Limited',
    'Skin Elements Limited',
    'Dragon Mountain Gold Limited',
    'Boadicea Resources Limited',
    'Uvre Limited',
    'Westar Resources Limited',
    'Ishares High Growth Esg ETF',
    'Ausmon Resources Limited',
    'Sacgasco Limited',
    'Great Northern Minerals Limited',
    'Xstate Resources Limited',
    'FAT Prophets Global High Conviction Hedge Fund',
    'Nucoal Resources Limited',
    'Hexima Limited',
    'Kaddy Limited',
    'TG Metals Limited',
    'Nickelsearch Limited',
    'Global X Usd Corporate Bond ETF (Currency Hedged)',
    'Dundas Minerals Limited',
    'Accent Resources NL',
    'Betashares Global Royalties ETF',
    'Optima Technology Group Limited',
    'Emperor Energy Limited',
    'Western Gold Resources Limited',
    'Heavy Rare EARTHS Limited',
    'Equity Trustees Limited',
    'Betashares Solar ETF',
    'Australian Bond Exchange Holdings Limited',
    'Redcastle Resources Limited',
    'TYMLEZ Group Limited',
    'Reedy Lagoon Corporation Limited',
    'Panther Metals Limited',
    'Activex Limited',
    'Cavalier Resources Limited',
    'Trigg Minerals Limited',
    'Simble Solutions Limited',
    'Remsense Technologies Limited',
    'REGENER8 Resources NL',
    'Harris Technology Group Limited',
    'Rocketboots Limited',
    'ZIMI Limited',
    'Timah Resources Limited',
    'Advance Metals Limited',
    'Exopharm Limited',
    'Equity Trustees Limited',
    'Mamba Exploration Limited',
    'I Synergy Group Limited',
    'Nexion Group Limited',
    'Sarama Resources Limited',
    'Middle Island Resources Limited',
    'Anatara Lifesciences Limited',
    'Bentley Capital Limited',
    'Perpetual Esg Australian Share Fund (Managed Fund)',
    'BPH Global Limited',
    'Carbine Resources Limited',
    'New Zealand Coastal Seafoods Limited',
    'Tali Digital Limited',
    'Peako Limited',
    'Acdc Metals Limited',
    'Golden Cross Resources Limited',
    'Sierra Nevada Gold Inc',
    'Pearl Gull Iron Limited',
    'DC Two Limited',
    'Nutritional Growth Solutions Limited',
    'Diablo Resources Limited',
    'Mec Resources Limited',
    'Global X Metal Securities Australia Limited',
    'Santa Fe Minerals Limited',
    'Avira Resources Limited',
    'Enterprise Metals Limited',
    'Ishares Future Tech Innovators ETF',
    '333D Limited',
    'Genesis Resources Limited',
    'Peak Minerals Limited',
    'Desert Metals Limited',
    'Global X Uranium ETF',
    'Icon Energy Limited',
    'Mount Burgess Mining NL',
    'Merchant House International Limited',
    'Techgen Metals Limited',
    'Propell Holdings Limited',
    'SQX Resources Limited',
    'KEY Petroleum Limited',
    'Lord Resources Limited',
    'Halo Food Co. Limited',
    'Holista Colltech Limited',
    'C29 Metals Limited',
    'Aurum Resources Limited',
    'Happy Valley Nutrition Limited',
    'Enova Mining Limited',
    'Intelicare Holdings Limited',
    'Eastern Metals Limited',
    'Culpeo Minerals Limited',
    'Octava Minerals Limited',
    'YPB Group Limited',
    'Forbidden Foods Limited',
    'Betashares Nasdaq 100 Yield MAX (Managed Fund)',
    'Perpetual Global Innovation Share (Managed Fund)',
    'Identitii Limited',
    'JAYEX Technology Limited',
    'Cosmo Metals Limited',
    'Global X S&P/ASX 200 Covered Call ETF',
    'Sagalio Energy Limited',
    'Global X Australia Ex Financials & Resources ETF',
    'Betashares Future of Payments ETF',
    'Betashares Metaverse ETF',
    'Killi Resources Limited',
    'Applyflow Limited',
    'VIP Gloves Limited',
    'Moho Resources Limited',
    'Dalaroo Metals Limited',
    'Inventis Limited',
    'Rincon Resources Limited',
    'Global X Green Metal Miners ETF',
    'Pinnacle Minerals Limited',
    'Oakajee Corporation Limited',
    'EMU NL',
    'Allup Silica Limited',
    'CYCLIQ Group Limited',
    'Regeneus Limited',
    'Betashares Future of Food ETF',
    'MT Malcolm Mines NL',
    'Milford Australian Absolute Growth (Hedge Fund)',
    'Oakridge International Limited',
    'TTA Holdings Limited',
    'Prominence Energy Limited',
    'Winchester Energy Limited',
    'Parkd Limited',
    'Betashares Video Games and Esports ETF',
    'Assetowl Limited',
    'Equity Story Group Limited',
    'Alice QUEEN Limited',
    'DMC Mining Limited',
    'DXN Limited',
    'Star Minerals Limited',
    'Orange Minerals NL',
    'Orion Equities Limited',
    'Ishares Balanced Esg ETF',
    'Global X Bloomberg Commodity ETF (Synthetic)',
    'Betashares Digital Health and Telemedicine ETF',
    'Aneka Tambang (Persero) TBK (PT)',
    'Armada Metals Limited',
    'Story-I Limited',
    'Mariner Corporation Limited',
    'Janus HDRSN ZR Trans Res Active ETF (Managed Fund)',
    'Wellfully Limited',
    'Kaili Resources Limited',
    'Cfoam Limited',
    'Raptis Group Limited',
    'Global X Global Carbon ETF (Synthetic)',
    'Invigor Group Limited',
    'Asaplus Resources Limited',
    'Global X Nasdaq 100 Covered Call ETF',
    'JPM US100Q EQ Prem Inc Active ETF (Managed Fund)',
    'Jpmorgan Climate CHG Sol Active ETF (Managed Fund)',
    'JPM US100Q EQ Prem Inc H Active ETF (Managed Fund)',
    'Equity Trustees Limited',
    'Catalano Seafood Limited',
    'JPM EQTY Prem Inc H Active ETF (Managed Fund)',
    'Jpmorgan Sustain Infra Active ETF (Managed Fund)',
    'Colortv Limited',
    'Munro Concentrated Global Growth (Managed Fund)',
    'Global X S&P 500 Covered Call ETF',
    'Equity Trustees Limited',
    'Betashares Online Retail and E-Commerce ETF',
    'ABRDN Sust Asian Opp Active ETF (Managed Fund)',
    'Janus Henderson GLB Sust Active ETF (Managed Fund)',
    'Equity Trustees Limited',
    'Global X US 100 ETF',
    'Bridge Saas Limited',
    'Laramide Resources Limited',
    'My Foodie BOX Limited',
    'Multistack International Limited',
    'Aurora Global Income Trust',
    'Queste Communications Limited',
    'Equity Trustees Limited',
    'Roots Sustainable Agricultural Technologies Limited',
    'Equity Trustees Limited',
    'Lawfinance Limited',
    'Janus Henderson Sust CR Active ETF (Managed Fund)',
    'Carlton Investments Limited',
    'EMU NL',
    'Sietel Limited',
    'Whitefield Industrials Limited', 'Cash - US Dollar'

                                                        
                                                        ]:
                                

                                word_instances = page.search_for(keyword_matched_amount)
                                
                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Investment Summary Report'
                                            second_word_Tofind = 'Market Value'
                                            subsequent_word = keyword_matched_amount
                                            

                                            matched_goto_pagenumber = None
                                            
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line: #1 value_to_find
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if second_word_Tofind in subsequent_line: #2 second_word_Tofind
                                                                for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                                    if subsequent_word in second_subsequent_line: #3 subsequent_word
                                                                        matched_goto_pagenumber = page_num
                                                                        break
                                                                    elif matched_goto_pagenumber is None:
                                                                        find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', second_subsequent_line)
                                                                        if find_decimal_value:
                                                                            # print(find_decimal_value)
                                                                            find_decimal_value = [value.replace(',','').strip() for value in find_decimal_value]
                                                                            for exact_decimal_value in find_decimal_value:
                                                                            
                                                                                if exact_decimal_value != 0.00:

                                                                                    convert_ToInt_subsequent_word = subsequent_word.replace(',','').strip()

                                                                                    round_value = round(float(convert_ToInt_subsequent_word))

                                                                                    decimal_value = float(exact_decimal_value)
                                                                                
                                                                                    if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                                        matched_goto_pagenumber = page_num
                                                                                        keyword_matched_amount = f"{decimal_value:,.2f}"
                                                                                    
                                                                                        break 
                                                                            
                                                if matched_goto_pagenumber is not None:
                                                    break
                                                                        
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            # page = pdf.pages[matched_goto_pagenumber]
                                            
                                            # texts = page.extract_text().split('\n')
                                            # for text in texts:
                                            #     if subsequent_word in text:
                                            #         data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                            #         if data:

                                            #             matched_data = data[-1]
                                            doc = fitz.open(pdf_path)
                                            matched_page = doc[matched_goto_pagenumber]

                                            keyword = keyword_matched_amount
                                        
                                
                                            word_instances = matched_page.search_for(keyword)
                                            if len(word_instances) > 0:

                                                x, y, x1, y1 = word_instances[-1]

                                                page_height = matched_page.rect.height

                                                # Calculate the new y-coordinate for the bottom placement
                                                new_y = page_height - y1
                                                pdf_writer.addLink(
                                                    matched_goto_pagenumber,
                                                    page_no_to_palce_link,
                                                    RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                    border=[1, 1, 1]
                                                )
                                                tentative_matched_amount = None
                                                break
                                        except Exception as e:
                                        
                                            Link_notGenerated.append(word)
                                            pass    
                            
                            elif matched_word_string == 'ANZ - E*trade Cash Investment Account' or matched_word_string == 'CBA Direct Investment Account':
                                
                                word_instances = page.search_for(keyword_matched_amount)

                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        try:
                                            page_height = page.rect.height
                                            new_y = page_height - y1

                                            value_to_find = 'Cash transactions'
                                            subsequent_word = keyword_matched_amount

                                            matched_goto_pagenumber = None
                                            for page_num, page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if value_to_find in line:
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if subsequent_word in subsequent_line:
                                                                matched_goto_pagenumber = page_num
                                                                break
                                            pdf_writer.addLink(
                                                page_no_to_palce_link,
                                                matched_goto_pagenumber,
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                border = [1,1,1]
                                            )
                                            
                                            # page = pdf.pages[matched_goto_pagenumber]
                                            
                                            # texts = page.extract_text().split('\n')
                                            # for text in texts:
                                            #     if subsequent_word in text:
                                            #         data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)

                                            #         if data:

                                            #             matched_data = data[-1]
                                            doc = fitz.open(pdf_path)
                                            matched_page = doc[matched_goto_pagenumber]

                                            keyword = keyword_matched_amount

                                            word_instances = matched_page.search_for(keyword)
                                            if len(word_instances) > 0:
                                                x,y,x1,y1 = word_instances[-1]
                                                page_height = matched_page.rect.height

                                                new_y = page_height - y1
                                                pdf_writer.addLink(
                                                    matched_goto_pagenumber,
                                                    page_no_to_palce_link,
                                                    RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                    border=[1,1,1]
                                                )
                                                break
                                        except Exception as e:
                                    
                                            Link_notGenerated.append(word)
                                            pass    
                            
                            else:
                                word_instances = page.search_for(keyword_matched_amount)
                                if len(word_instances) > 0:
                                    for instance in word_instances:
                                        x, y, x1, y1 = instance
                                        
                                        #Get the height of the page
                                        try:
                                            page_height = page.rect.height

                                            #Calculate the new y-coordinates for the bottom placement
                                            new_y = page_height - y1

                                            #Add a link to the new PDF using the updated coordinates
                                            first_word_Tofind = 'General Ledger'

                                            if (word == 'Employer Contributions' or word == 'Personal Non Concessional' or word == 'Personal Concessional' or word == 'Other Contributions'):
                                                second_word_Tofind = 'Contributions'
                                            else:    
                                                second_word_Tofind = word

                                            if word in word_based_credits:
                                                third_word_Tofind = 'Total Credits'
                                            else:
                                                third_word_Tofind = 'Total Debits'
                                            
                                            #To find the above mentioned data from the pdf 
                                            matched_goto_pagenumber = None
                                            for page_num , page in enumerate(pdf.pages):
                                                lines = page.extract_text().split('\n')
                                                for line in lines:
                                                    if first_word_Tofind in line: #1
                                                        for subsequent_line in lines[lines.index(line) + 1:]:
                                                            if second_word_Tofind in subsequent_line: #2                                                        
                                                                for second_subsequent_line in lines[lines.index(subsequent_line) + 1:]:
                                                                    if third_word_Tofind in second_subsequent_line: #3                                                             
                                                                        matched_goto_pagenumber = page_num
                                                                        break
                                                                    elif matched_goto_pagenumber is None:
                                                                        find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', second_subsequent_line)
                                                                        if find_decimal_value:
                                                                            find_decimal_value = [value.replace(',','').strip() for value in find_decimal_value]
                                                                            for exact_decimal_value in find_decimal_value:

                                                                                if exact_decimal_value != 0.00:

                                                                                    convert_ToInt_subsequent_word = keyword_matched_amount.replace(',', '').strip()

                                                                                    round_value = round(float(convert_ToInt_subsequent_word))

                                                                                    decimal_value = float(exact_decimal_value)

                                                                                    if (decimal_value <= round_value + 1 and decimal_value >= round_value -1):
                                                                                        matched_goto_pagenumber = page_num
                                                                                        keyword_matched_amount = f"{decimal_value:,.2f}"
                                                                                        break

                                                #this if statement is used for next page to find the third word because it can't find means it goes to next page
                                                if matched_page_number is not None:
                                                    i = page_num + 1
                                                    for data in enumerate(pdf.pages):
                                                        next_line = pdf.pages[i].extract_text().split('\n')
                                                        for end_line in next_line:
                                                            if third_word_Tofind in end_line:
                                                                for end_line in next_line:
                                                                    if keyword_matched_amount in end_line:
                                                                        matched_goto_pagenumber = i
                                                                        break
                                                                    elif matched_goto_pagenumber is None:
                                                                        find_decimal_vlaue = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', second_subsequent_line)
                                                                        if find_decimal_value:
                                                                            find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                                            for exact_decimal_value in find_decimal_value:
                                                                                if exact_decimal_value != 0.00:
                                                                                    convert_ToInt_subsequent_word = keyword_matched_amount.replace(',', '').strip()

                                                                                    round_value = round(float(convert_ToInt_subsequent_word))

                                                                                    decimal_value = float(exact_decimal_value)

                                                                                    if (decimal_value <= round_value + 1 and decimal_value >= round_value -1):
                                                                                        matched_goto_pagenumber = page_num
                                                                                        keyword_matched_amount = f"{decimal_value:,.2f}"
                                                                                        break

                                                        if matched_goto_pagenumber is None:
                                                            i += 1
                                                        else:
                                                            break
                                                    break
                                                        
                                            #to generate top link of the pdf
                                            pdf_writer.addLink(
                                                page_no_to_palce_link, #top page to palce link
                                                matched_goto_pagenumber, #Bottom page to place link
                                                RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]), #rectangel box for the matched data
                                                border=[1, 1, 1]    #color of the rectangle box
                                            )

                                            #Below code is used for generate bottom link of the pdf

                                            page = pdf.pages[matched_goto_pagenumber]

                                            texts = page.extract_text().split('\n')
                                            for text in texts:
                                                if third_word_Tofind in text:
                                                    data = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', text)  
                                                    if data:
                                                        matched_data = data[0]
                                                        #this if for matching the same amount is equal to actual amount in total credits or debits
                                                        if matched_data ==  keyword_matched_amount:  
                                                        
                                                            doc = fitz.open(pdf_path)
                                                            matched_page = doc[matched_goto_pagenumber]
                                                            #
                                                            keyword = matched_data
                                                            word_instances = matched_page.search_for(keyword)
                                                            if len(word_instances) > 0:

                                                                x, y, x1, y1 = word_instances[-1]

                                                                page_height = matched_page.rect.height

                                                                #calculate the new y-coordinate for the bottom placement
                                                                new_y = page_height - y1
                                                                pdf_writer.addLink(
                                                                    matched_goto_pagenumber,
                                                                    page_no_to_palce_link,
                                                                    RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                    border=[1, 1, 1]
                                                                )
                                                                break
                                                        #else if for the amount is not equal means it place the link in last index of matched amount 
                                                        else:
                                                        
                                                            doc = fitz.open(pdf_path)
                                                            matched_page = doc[matched_goto_pagenumber]

                                                            #
                                                            keyword = keyword_matched_amount
                                                        
                                                            word_instances = matched_page.search_for(keyword)
                                                            if len(word_instances) > 0:

                                                                x, y, x1, y1 = word_instances[-1]

                                                                page_height = matched_page.rect.height

                                                                #calculate the new y-coordinate for the bottom placement
                                                                new_y = page_height - y1
                                                                pdf_writer.addLink(
                                                                    matched_goto_pagenumber,
                                                                    page_no_to_palce_link,
                                                                    RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                                                    border=[1, 1, 1]
                                                                )
                                                                break

                                        except Exception as e:
                                        
                                            Link_notGenerated.append(word)
                                            pass           
                                        
                                # else:
                                #     Link_notGenerated.append(word)
                    #Below code only for memeber statement - Start

                    #variable statement to find the sentence in the pdf from start account to end account variable in between member *amount
                    start_account = "Liability for accrued benefits allocated to members' accounts"
                    end_account = "Total Liability for accrued benefits allocated to members' accounts"

                    #To store the amount and page no. as a dictionary data structure
                    matched_client_values = {}

                    #Gather the inbetween amount and page no.
                    for page_num, page in enumerate(pdf.pages):
                        lines = page.extract_text().split('\n')
                        for line in lines:
                            if start_account in line:
                                # If start_account is  matched, search for end_account in subsequent lines
                                matched_page_number = []
                                data_lines = []
                                for subsequent_line in lines[lines.index(line) + 1:]:
                                    # values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))', subsequent_line)
                                    values = re.findall(r' \b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))(?![0-9]{2}/[0-9]{2}/[0-9]{4})(?![0-9]{2}:[0-9]{2}:[0-9]{2})', subsequent_line)
                                
                                    if values: 
                                        compare_val = values[0].replace(',', '').strip()
                                        if float(compare_val) > 300: 
                                            data_lines.append(values[0])
                                            matched_page_number.append(page_num)
                                    if end_account in subsequent_line:
                                        #If end_account is found, extract the data from the collected lines
                                        matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                        break #Exit the loop if end_account is found
                                    else:
                                        nextPage = page_num + 1
                                        lines = pdf.pages[nextPage].extract_text().split('\n')
                                        for line in lines:
                                            # values = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))', line)
                                            values = re.findall(r' \b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![^()]*\))(?![0-9]{2}/[0-9]{2}/[0-9]{4})(?![0-9]{2}:[0-9]{2}:[0-9]{2})', line)
                                        
                                            if values:
                                                compare_val = values[0].replace(',', '').strip() 
                                                if float(compare_val) > 300:
                                                    data_lines.append(values[0])
                                                    matched_page_number.append(nextPage)
                                            if end_account in line:
                                                matched_client_values[start_account] = (data_lines[:-1], matched_page_number[:-1])
                                                break
                                break #Exit the loop if start_account is found
                            
                    # print all matched data and their respective page numbers - for client member' account benefits

                    #find out the above matched value with below specified member_statementSring value  and place the top link
                    for start, (data, client_name_page) in matched_client_values.items():
                        
                        for line_data, client_pageNo in zip(data, client_name_page):
                
                            doc = fitz.open(pdf_path)
                            matched_client_page = doc[client_pageNo]
                            client_nameTo_placeLink = client_pageNo
                        
                            client_data_no = line_data
                            member_statementString = 'Members Statement'
                            matched_memberPageNo = None

                            for page_num, page in enumerate(pdf.pages):
                                lines = page.extract_text().split('\n')
                                for line in lines:
                                    if member_statementString in line:
                                        for member_subsequent_line in lines[lines.index(line) + 1:]:
                                            if line_data in member_subsequent_line:
                                                matched_memberPageNo = page_num
                                                break
                                            elif matched_memberPageNo is None:
                                                find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', member_subsequent_line)
                                                if find_decimal_value:
                                                    find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                    for exact_decimal_value in find_decimal_value:
                                                        if exact_decimal_value != 0.00:
                                                            convert_ToInt_subsequent_word = line_data.replace(',', '').strip()
                                                            round_value = round(float(convert_ToInt_subsequent_word))
                                                            decimal_value = float(exact_decimal_value)

                                                            if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                matched_memberPageNo = page_num
                                                                client_data_no_decimal = f"{decimal_value:,.2f}"
                                                            
                                                                break
                                                            

                                if matched_memberPageNo is None:
                                    i = page_num + 1
                                    for date in enumerate(pdf.pages):
                                        try:
                                            next_line = pdf.pages[i].extract_text().split('\n')
                                            for end_line in next_line:
                                                if member_statementString in end_line:
                                                    for subsequent_line in next_line[next_line.index(end_line) + 1:]:
                                                        if line_data in subsequent_line:
                                                            matched_memberPageNo = i
                                                            break
                                                        elif matched_memberPageNo is None:
                                                            find_decimal_value = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', member_subsequent_line)
                                                            if find_decimal_value:
                                                                find_decimal_value = [value.replace(',', '').strip() for value in find_decimal_value]
                                                                for exact_decimal_value in find_decimal_value:
                                                                    if exact_decimal_value != 0.00:
                                                                        convert_ToInt_subsequent_word = line_data.replace(',', '').strip()
                                                                        round_value = round(float(convert_ToInt_subsequent_word))
                                                                        decimal_value = float(exact_decimal_value)

                                                                        if (decimal_value <= round_value + 1 and decimal_value >= round_value - 1):
                                                                            matched_memberPageNo = page_num
                                                                            client_data_no_decimal = f"{decimal_value:,.2f}"

                                                                            break

                                            if matched_memberPageNo is None:
                                                i += 1
                                            else:
                                                break
                                        except:
                                            pass

                                        break

                            word_instance = matched_client_page.search_for(client_data_no)
                
                            if len(word_instance) > 0:
                                for instance in word_instance:
                                    x,y, x1,y1 = instance
                                    try:
                                        page_height = matched_client_page.rect.height

                                        new_y = page_height - y1

                                        pdf_writer.addLink(
                                            client_nameTo_placeLink,
                                            matched_memberPageNo,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border=[1,1,1]
                                        )
                                    except Exception as e:
                                    
                                        pass
                            
                            #This for below matched amount to set bottom to top link in the pdf
                            doc = fitz.open(pdf_path)
                            if matched_memberPageNo is not None:
                            
                                matched_client_page_up = doc[matched_memberPageNo]
                                word_instance = matched_client_page_up.search_for(client_data_no)
                                if not word_instance:
                                    client_data_no_decimal = client_data_no_decimal.replace(',', '').strip()
                                    convert_to_int = int(float(client_data_no_decimal))
                                    print(convert_to_int)
                                    client_data_no = f"{convert_to_int:,}"
                                    print(client_data_no)
                                word_instance = matched_client_page_up.search_for(client_data_no)
                                print(word_instance)
                                if len(word_instance) > 0:
                                    
                                    try:
                                        x,y, x1,y1 = word_instance[-2]
                                        page_height = matched_client_page_up.rect.height

                                        new_y = page_height - y1

                                        pdf_writer.addLink(
                                            matched_memberPageNo,
                                            client_nameTo_placeLink,
                                            RectangleObject([x-10, new_y, x1+10, (new_y + (y1 - y))]),
                                            border=[1,1,1]
                                        )
                                    except Exception as e:
                                    
                                        pass

                                else:
                                    print('Word not found in the PDF')

                    #End memeber statement 
                    # Link_notGenerated.pop(-2)
                    # print(Link_notGenerated)
                    
                    # save the modified PDF
                    filename = os.path.splitext(pdf_file)[0] #Extract the filename without extension
                    output_file = path.join(path_folder, f'Automated_link_{filename}.pdf')

                    # output_file_error_log = path.join(path_folder, f'Error_log_File_{filename}.txt')
                    # with open(output_file_error_log, 'w') as file:
                    #     file.write("_______________ Failing to generate link for this below Word's _______________"+'\n')
                    #     file.write('\n')
                    #     for item in Link_notGenerated:
                    #         file.write(item + '\n')
                    #         file.write('\n')
                    # print(f'Data has been written to {output_file_error_log}')

                    with open(output_file, 'wb') as link_pdf:
                        pdf_writer.write(link_pdf)
                    print(f'Link added to the PDF: {output_file}')                           
                                                    

    else:
        print('Password is Incorrect!')
        pdf_automation()

pdf_automation()

