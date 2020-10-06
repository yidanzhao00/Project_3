'use strict';
var myToken;



// Close dialog with the customer, reporting fulfillmentState of Failed or Fulfilled ("Thanks, your Requested Info will be Processed Soon")
function close(sessionAttributes, fulfillmentState, content, callback) {
    console.log("WHY")
    
   //if (err) {
    //    console.log(err.stack);
  //  }
   // else {
        console.log("Calling back now")
        console.log(callback.toString())
       
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillmentState,
            "message": {
      "contentType": "PlainText",
      "content": content
    },
    
//}
}}
}


function delegate(session_attributes, slots, address, callback) {
    
    return {
        
        'dialogAction': {
            'type': 'Delegate',
            'slots': {
                'contractAddress': address,
                "acctName": slots.acctName,
                "bankNumber": slots.bankNumber,
                "acctType": slots.acctType
        }
    }}

    //return response;
}

 
async function RetrieveBalance(event, contract1, callback) {
    //var version = web3.version.api;
    console.log("RETRIEVE");
    var source = event.invocationSource;
    var address=await contract1.options.address;
    var name=event.currentIntent.slots.acctName;
    var branchNumber=event.currentIntent.slots.bankNumber;
    var accountType=event.currentIntent.slots.acctType;
    var accountCode;
    
    switch (accountType) {
        case 'Personal':
            accountCode=0;
            break;
        case 'Business':
            accountCode=1;
            break;
        case 'Joint':
            accountCode=2;
            break;
        default:
            console.log("Error");
            
    }
    if (source=="DialogCodeHook") {
        
        return delegate(event.sessionAttributes, event.currentIntent.slots, address, callback);
    }
    else {
        
  var balance=await contract1.methods.getAcctBalByName(name, accountCode, branchNumber).call();
  //then(result => close(event.sessionAttributes, 'Fulfilled', `Your balance is ${result}`, callback));
  
  console.log("Just here")
  var message= `Your balance is ${balance}`;
  //console.log(message)
  return close(event.sessionAttributes, 'Fulfilled', message, callback);
    
        
    }
}
 
// --------------- Events -----------------------
 
function dispatch(event, contract1, callback) {
    console.log(`request received for userId=${event.userId}, intentName=${event.currentIntent.name}`);
    const sessionAttributes = event.sessionAttributes;
    const slots = event.currentIntent.slots;
    var source = event.invocationSource;
    
//    const psc_address = slots.contractAddress;
    
//    const crust = slots.crust;
//    const size = slots.size;
//   const pizzaKind = slots.pizzaKind;
    var intent_name = event.currentIntent.name;
    

    
    if (intent_name == "ProjectContractBalance") {
        return RetrieveBalance(event, contract1, callback);
}
    else if (intent_name=='ProjectContractRules') {

  var toReturn=contract1.methods.getBranchName(0).call().then(console.log);
   
    
    console.log(close(sessionAttributes, 'Fulfilled',
    {'contentType': 'PlainText', 'content': `Be Patient and have this while we are working on it,
    The current balance in the Smart Contract with Address ID is ${toReturn}`}));
    
   
}
};
 
// --------------- Main handler -----------------------
 
function LambdaCallback(err, result) {
    console.log("In LAMBDA CALLBACK");
 if (err) {
        console.log(err.stack);
    }
 else {
     console.log("REturning")
     return result;
 }
}

var https = require('https'); 
const fs=require('fs');
var path=require("path");
const Web3=require('web3');
exports.handler = (event, context, LambdaCallback) => {
   
    
    console.log(LambdaCallback.toString())
    var web3=new Web3(new Web3.providers.HttpProvider('https://kovan.infura.io/v3/b2b0259ccd7541938a412ecf9ea62ff1'));
  var jsonData2;
  //console.log(__dirname);
  console.log(path.resolve('CryptoFax.json'));
  var address=event.currentIntent.slots.contractAddress;
  //process.cwd();
  jsonData2=JSON.parse(fs.readFileSync('CryptoFax.json', 'utf-8'));
  var contract1=new web3.eth.Contract(jsonData2, address, {
          from: '0xfF2b256E189e093503a14a12141CA33Fc8AA54e2'
  });
    
    
    return dispatch(event, contract1, LambdaCallback);
    
}



