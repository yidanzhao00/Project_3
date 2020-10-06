### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
import boto3
import json
#----------------------------------------------#
# Global Variables

sc_name = "Joint Savings"
sc_tokens = "ETH, ARCD, LINK"
sc_eth2usd = "1 ETH = 201 USD"
sc_link2usdk = "1 LINK = 202 USD"
sc_tools = "WEB3, Remax, Solidity, MetaMask, Ganache"
sc_actions = "Create Account, Deposit, Withdraw, Get Balance, Send Ether, Transfer Ether"
sc_balance = "123.45 ETH"


project_coin_types = "ETH, ARCD, LINK and USD"

#----------------------------------------------#
### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")

#----------------------------------------------#
def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

#----------------------------------------------#
def validate_data1(pct_startdate, pct_amount, intent_request):
    """
    Validates the data provided by the user.
    """
    print("KS - from Function - validate_data1")
    todaysdate1 = datetime.now()
     
    #--------------------------------------------------#
    # V11 Validate that the date is not in the past
    print("KS - V11: User entered value for variable - pct_startdate:", pct_startdate)
    if pct_startdate is not None:
        # print("KS - Type of user entered date:", type(pct_startdate))
        # print("KS - Value of user entered date:", pct_startdate) 
        # string_input_with_date = pct_startdate # "25/10/2020"
        # userdate = datetime.strptime(string_input_with_date, "%Y-%m-%d") # "%m/%d/%Y")
        userdate_v11 = datetime.strptime(pct_startdate, "%Y-%m-%d") # "%m/%d/%Y")
        # userdate = datetime.datetime(pct_startdate)
        #### todaysdate = datetime.now()
        # print("KS - Type of user entered date after conversion:", type(userdate))
        # print("KS - Value of user entered date after conversion:", userdate)
        # print("KS - Type of system date:", type(todaysdate))
        # print("KS - Value of system date:", todaysdate)

        if userdate_v11.date() < todaysdate1.date():
            return build_validation_result(
                False,
                "pctStartDate",
                "should be either today or a future date, "
                "Please provide a valid date.",
            )
    #--------------------------------------------------#
    # V12 Validate the Contract amount, it should be > 0
    print("KS - V12: User entered value for variable - pct_amount:", pct_amount)
    if pct_amount is not None:
        pct_amount = parse_float(
            pct_amount
        )  # Since parameters are strings it's important to cast values
        if pct_amount <= 0:
            return build_validation_result(
                False,
                "pctAmount",
                "Contract amount should be greater than zero, "
                "Please provide a correct amount in USD to create a contract.",
            )
    #--------------------------------------------------#

    
    # A True results is returned when all variables entered are valid
    return build_validation_result(True, None, None)

#----------------------------------------------#
def validate_data2(pcc_startdate, pcc_enddate, intent_request):
    """
    Validates the data provided by the user.
    """
    print("KS - from Function - validate_data2")
    todaysdate2 = datetime.now()
     
    #--------------------------------------------------#
    # V21 Validate that the Start date is not in the past
    print("KS - V21: User entered value for variable - startDate:", pcc_startdate)
    if pcc_startdate is not None:
        userdate_v21 = datetime.strptime(pcc_startdate, "%Y-%m-%d") # "%m/%d/%Y")

        if userdate_v21.date() < todaysdate2.date():
            return build_validation_result(
                False,
                "startDate",
                "should be either today or a future date, "
                "Please provide a valid date.",
            )
    #--------------------------------------------------#
    #--------------------------------------------------#
    # V22 Validate that the End date is not in the past
    print("KS - V22: User entered value for variable - endDate:",pcc_enddate)
    if pcc_enddate is not None:
        userdate_v22 = datetime.strptime(pcc_enddate, "%Y-%m-%d") # "%m/%d/%Y")

        if userdate_v22.date() < todaysdate2.date():
            return build_validation_result(
                False,
                "endDate",
                "should be either today or a future date, "
                "Please provide a valid date.",
            )
    #--------------------------------------------------#
    #--------------------------------------------------#
    #--------------------------------------------------#
    #--------------------------------------------------#
    #--------------------------------------------------#
    
    # A True results is returned when all variables entered are valid
    return build_validation_result(True, None, None)

#----------------------------------------------#

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]
    
#----------------------------------------------#
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }

#----------------------------------------------#
def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }
#----------------------------------------------#
def close(intent_request, session_attributes, fulfillment_state, message):
# def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

#----------------------------------------------#
### Intents Handlers ###
def projectcontracttest(intent_request):
    """
    Performs dialog management and fulfillment for contract test.
    """

    # Gets slots' values
    pct_startdate = get_slots(intent_request)["pctStartDate"]
    pct_amount = get_slots(intent_request)["pctAmount"]

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]  #

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data1(pct_startdate, pct_amount, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))


    # Return a message with conversion's result.
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for your information;
            your Smart contract will be created on {} for an Amount of {} USD.
            """.format(
                pct_startdate, pct_amount
            ),
        },
    )
#----------------------------------------------#
def projectcointypes(intent_request):
    """
    Performs fulfillment for listing the Coint Types
    """
    
    """
    print("From Function: projectcointypes:")
    print(" INTENT REQUEST IS")
    print(intent_request)
    print("Invocation Source is: ")    
    print(intent_request['invocationSource'])
    

    print("Our Coint Type consists of these entries")
    print(project_coin_types)
    """
    
    
    if intent_request['invocationSource']=='DialogCodeHook':
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    

    # Return a message with the list of Coin Types
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Our Coin Types:  {project_coin_types}"
            
        }
    )
#----------------------------------------------#
def projectcontractbalance(intent_request):
    """
    Performs fulfillment for Contract Balance
    """

    # Gets slots' values
    pcc_contractaddress = get_slots(intent_request)["contractAddress"]

    if intent_request['invocationSource']=='DialogCodeHook':
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    

    # Return a message with the Contract Balance
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """
            The Balance for Smart Contact with Address ID: {} is {}
            """.format(
                pcc_contractaddress, sc_balance
            )
        }
    )



#-----------------------------------#
#-----------------------------------#
#-----------------------------------#



#-----------------------------------#
#-----------------------------------#
#-----------------------------------#
#----------------------------------------------#
#----------------------------------------------#    
#----------------------------------------------#
def projectcontractfees(intent_request):
    """
    Performs fulfillment for Contract Fees
    """
    
    """
    print("From Function: projectcontractfees:")
    print(" INTENT REQUEST IS")
    print(intent_request)
    print("Invocation Source is: ")    
    print(intent_request['invocationSource'])
    

    print("Our Contract Execution Fees is 2% of Contract Amount")
    print("Our Contract Cancellation Fees is 1% of Contract Amount")
    print("Our Penalty is 1% of Contract Amount")
    print("and all Fee payable either in USD or Coin Type of the Contract")
    """
    
    
    if intent_request['invocationSource']=='DialogCodeHook':
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    

    # Return a message with the Contract Fees
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Our Contract Fees is 2%, Cancellation Fee is 1% and Penalty is 1% of the Contract Amount either in USD or Tokens"
            
        }
    )

#----------------------------------------------#
#----------------------------------------------#
#----------------------------------------------#
#----------------------------------------------#
#----------------------------------------------#
def projectcontractperiod(intent_request):
    """
    Performs fulfillment for Contract Period
    """
    
    """
    print("From Function: projectcontractperiod:")
    print(" INTENT REQUEST IS")
    print(intent_request)
    print("Invocation Source is: ")    
    print(intent_request['invocationSource'])
    
    print("Our Contract runs from ", startDate, " to ", endDate)

    """
    
    if intent_request['invocationSource']=='DialogCodeHook':
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    

    # Return a message with the Contract Dates
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Please BE PATIENT, we are working on this function - projectcontractperiod!"
        }
    )
#----------------------------------------------#
#----------------------------------------------#
#----------------------------------------------#
#----------------------------------------------#
def projectcontractrules(intent_request):
    """
    Performs fulfillment for Contract Rules
    """
    
    """
    print("From Function: projectcontractfees:")
    print(" INTENT REQUEST IS")
    print(intent_request)
    print("Invocation Source is: ")    
    print(intent_request['invocationSource'])
    

    print("Our Contract Rules are specified in the digital document")
    print("and has digital signature on the document from all parties involved")

    """
    
    
    if intent_request['invocationSource']=='DialogCodeHook':
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    

    # Return a message with the Contract Fees
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Our Contract Rules are specified in the digital document and can be executed as low as 1 day and can close as soon as the goal met."
        }
    )

#----------------------------------------------#
def projectcreatecontract(intent_request):
    """
    Performs dialog management and fulfillment for Contract Creation.
    """

    # Gets slots' values
    pcc_receivername   = get_slots(intent_request)["receiverName"]
    pcc_sendername     = get_slots(intent_request)["senderName"]
    pcc_assetname      = get_slots(intent_request)["assetName"]
    pcc_assetprice     = get_slots(intent_request)["assetPrice"]    
    pcc_currencytype   = get_slots(intent_request)["currencyType"]
    pcc_startdate      = get_slots(intent_request)["startDate"]
    pcc_enddate        = get_slots(intent_request)["endDate"]
    pcc_contractperiod = get_slots(intent_request)["contractPeriod"]

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]  #

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data2(pcc_startdate, pcc_enddate, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))


    # Return a message with conversion's result.
    return close(
        intent_request,
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for your information;
            your Smart contract will be created on {} with an end date of  {}
            from Sender {} to Receiver {} 
            for Asset {} for {} of Currency Type {}
            and the Contract Period is {} days
            """.format(
                pcc_startdate, pcc_enddate, 
                pcc_receivername,  pcc_sendername,
                pcc_assetname, pcc_assetprice, pcc_currencytype,
                pcc_contractperiod

            )
        }
    )
#----------------------------------------------#
#----------------------------------------------#

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    
    print("KS - from Function - dispatch (Intents Dispatcher)")
    # print("KS - Current Intent Request:", intent_request)

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    print("KS - Current Intent Name:", intent_name)
    
    # Dispatch to bot's intent handlers
    if intent_name == "ProjectCoinTypes":
        return projectcointypes(intent_request)

    elif intent_name == "ProjectContractFees":
        return projectcontractfees(intent_request)

    elif intent_name == "ProjectContractPeriod":
        return projectcontractperiod(intent_request)
        
    elif intent_name == "ProjectContractRules":
        return projectcontractrules(intent_request)
        
    elif intent_name == "projectContractTest":
        return projectcontracttest(intent_request)        
        
    elif intent_name == "ProjectCreateContract":
        return projectcreatecontract(intent_request)   
        
    elif intent_name == "ProjectContractBalance":
        return projectcontractbalance(intent_request)          
        
    raise Exception("Intent with name " + intent_name + " not supported")

#----------------------------------------------#
### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    print("KS - from Function - lambda_handler (Main Handler)")
    print("KS - Event:", event)
    print("KS - Context:", context)


    return dispatch(event)

#----------------------------------------------#
