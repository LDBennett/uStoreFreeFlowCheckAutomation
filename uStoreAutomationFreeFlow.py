#This program uses the splinter tool to use the browser
#in a particular way for the XMPie program uStore.
#This one loops through given product IDs and changes
#them to default in the FreeFlow section of each product.

from splinter import Browser

#Login to uStore / Goes to page, filles UN and PW and submits
def login(user,password):
	print("Logging in")
	browser.visit('https://us514.agstorefront.com/uStoreAdmin/login.aspx')
	browser.fill('ctl00$cphMainContent$txtUser', user)
	browser.fill('ctl00$cphMainContent$txtPassword', password)
	browser.click_link_by_id('ctl00_cphMainContent_btnLogin')
	print("Log in Successful")

#list all of the products in the store
def listAll(store):
	browser.visit('https://us514.agstorefront.com/uStoreAdmin/ProductList.aspx?storeID='+store)
	browser.click_link_by_id('ctl00_cphMainContent_lbtnAllProducts')
	print("Begining to retrieve the list of products")

#Retrieves all the product IDs from the store
def getAllProductIDs():
	list = browser.find_by_id('ctl00_cphMainContent_ProductListGrid_ctl00').find_by_tag('tbody').find_by_css('.rgSorted')
	pIDs = []

	index = 0
	while index < len(list):
		pIDs.append(list[index].value)
		index += 1
	
	print("Product IDs acquired")
	return pIDs
	
#places product online
def placeOnline(x):
	browser.visit(baseLink+str(x))
	browser.click_link_by_id('ctl00_cphMainContent_btnOnline')
	
#places product offline
def placeOffline(x):
	browser.visit(baseLink+str(x))
	browser.click_link_by_id('ctl00_cphMainContent_btnOffline')

#If product is online, checks FreeFlow status and changes it
#Skips if product is offline and skips if there is no FreeFlow 
def addFreeFlow(x):
	browser.visit(baseLink+str(x))
	status = browser.find_by_id('ctl00_cphMainContent_txtStatus').value
	profileLink = browser.is_element_present_by_id('ctl00_cphMainContent_linkedProfileAnnotation_lblAnnotation')

	if status == "Online" and profileLink == False:
		print("Placing Product: " + x + " Offline")
		browser.click_link_by_id('ctl00_cphMainContent_btnOffline')
		browser.click_link_by_id('ctl00_cphMainContent_btnImgPrepress')
		try:
			browser.check('ctl00$cphMainContent$ctl03$dgPrepressWorkflows$ctl00$ctl04$chkDefaultWorkflow')
			print ("Changing workflow status to DEFAULT")
		except:
			print("NO WORKFLOW FOUND...\nGoing to next product...")
		
		browser.click_link_by_id('ctl00_cphButtons_lblSave')
		print("Workflow SAVED")
		browser.click_link_by_id('ctl00_cphMainContent_btnOnline')
		print("Placing Product: " + x + " Online")
	else:
		print("Product ID: " + x + " Already Offline/Linked to Profile--->Product SKIPPED!")
		
#2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 35, 36, 37, 39, 40, 41, 42, 50, 51, 54, 55, 60, 61, 62, 63, 64, 66, 67, 68, 69, 71, 72, 73, 76, 86

storeIds = [40, 41, 42, 50, 54, 55, 60, 61, 62, 63, 64, 66, 67, 68, 69, 71, 72, 73, 76, 86]

userName = "USER NAME"
password = "PASSWORD"

for store in storeIds:
	storeS = str(store)
	print("Starting Browser Instance")
	browser = Browser('firefox',headless=True)
	login(userName,password)
	baseLink = "LINK  HERE"+storeS+"&productID="
	print("Store ID: " + storeS + " in progress...")

	listAll(storeS)

	products = getAllProductIDs()

	for item in products:
		addFreeFlow(item)

	print("Store ID: " + storeS + " complete\nClosing Browser Instance\n\n")
	browser.quit()


#for nums in productIds:
	#placeOnline(nums)
