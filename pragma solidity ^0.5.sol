pragma solidity ^0.5.0;
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/math/SafeMath.sol";
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol";
contract Bank {
    
    using Counters for Counters.Counter;
    Counters.Counter Branch_ID;
    
    string BankName;
    mapping(uint => Branch) Branches;
    
    
    constructor (string memory _BankName) public {
        BankName=_BankName;
    }
    
    event AddedBranch(string branchName, uint branchNumber);
    
    function createBranch(string memory branchName) public {
        Branches[Branch_ID.current()]=new Branch(branchName, Branch_ID.current());
        emit AddedBranch(branchName, Branch_ID.current());
        Branch_ID.increment();
        
    }
    
    
    function getBranchName(uint branchNumber) public view returns(string memory) {
        return Branches[branchNumber].getName();
    }
    
    function createAccount(uint choice, uint branchNumber, string memory _Name) internal {
        Branches[branchNumber].createAccount(choice, _Name);
    }
}
contract Branch {
    
    using Counters for Counters.Counter;
    Counters.Counter Account_ID;
    
    string BranchName;
    uint BranchNumber;
    mapping(uint => PersonalAccount) Personals;
    mapping(uint => BusinessAccount) Businesses;
    enum AccountType {Personal, Business}
    event AddedAccount(uint AccountNumber, string AccountName);
    
    constructor(string memory _BranchName, uint branchNumber) public {
        BranchName=_BranchName;
        BranchNumber=branchNumber;
    }
    
    function getAccountByAddress(uint choice, address account) public view {
        uint index=0;
        while (index<choice) {
            index++;
        }
        if (index==0) {
            PersonalAccount person=PersonalAccount(account);
        }
        
    }
    function getName() public view returns(string memory) {
        return BranchName;
    }
    
    function createAccount(uint choice, string memory _Name) public {
        uint index=0;
        while (index<choice) {
            index++;
        }
        if (index==0) {
            Personals[Account_ID.current()]=new PersonalAccount(Account_ID.current(), _Name);
        }
        else {
            Businesses[Account_ID.current()]=new BusinessAccount(Account_ID.current(), _Name);
        }
        emit AddedAccount(Account_ID.current(), _Name);
        Account_ID.increment();
    }
}
contract Accounts {
    uint accountID;
    string Name;
    
    constructor(uint _Num, string memory _Name) public {
        accountID=_Num;
        Name=_Name;
    }
}
contract PersonalAccount is Accounts {
    
    constructor(uint _Num, string memory _Name) Accounts(_Num, _Name) public {
        
    }
    address payable account_owner;
    uint public last_withdraw_block;
    uint public last_withdraw_amount;
    
    function withdraw(uint amount) public {
        require(msg.sender == account_owner);
        msg.sender.transfer(amount);
    }
    
    function transfer(address recipient, uint amount) public {
        address payable recipient;
        require(msg.sender == account_owner);
        recipient.transfer(amount);
    }   
    
    
    }

contract BusinessAccount is Accounts {
    constructor(uint _Num, string memory _Name) Accounts(_Num, _Name) public {
    }
    
    address payable account_owner;
    uint public last_withdraw_block;
    uint public last_withdraw_amount;
    
    address public last_to_deposit;
    uint public last_deposit_block;
    uint public last_deposit_amount;
    
    function withdraw(uint amount) public {
        require(msg.sender == account_owner);
        msg.sender.transfer(amount); 
    }
    
    function deposit() public payable {

        if (last_to_deposit != msg.sender) {
        last_to_deposit = msg.sender;
    }

        last_deposit_block = block.number;
        last_deposit_amount = msg.value;
    }
    
    function getBal()
    
}
contract JointSavings{
    address payable account_one;
    address payable account_two;

    address public last_to_withdraw;
    uint public last_withdraw_block;
    uint public last_withdraw_amount;

    address public last_to_deposit;
    uint public last_deposit_block;
    uint public last_deposit_amount;

    uint unlock_time;

    constructor(address payable _one, address payable _two) public {
        account_one = _one;
        account_two = _two;
    }
    function withdraw(uint amount) public {
        require(unlock_time < now, "Account is locked!");
        require(msg.sender == account_one || msg.sender == account_two, "You don't own this account!");

        if (last_to_withdraw != msg.sender) {
        last_to_withdraw = msg.sender;
        }

        last_withdraw_block = block.number;
        last_withdraw_amount = amount;

        if (amount > address(this).balance / 3) {
        unlock_time = now + 24 hours;
    }

    msg.sender.transfer(amount);
  }

    function deposit() public payable {

        if (last_to_deposit != msg.sender) {
        last_to_deposit = msg.sender;
    }

        last_deposit_block = block.number;
        last_deposit_amount = msg.value;
    }

  function() external payable {}
}