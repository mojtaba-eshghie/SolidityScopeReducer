

pragma solidity 0.5.17;

library SafeMath {
    








    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }

    








    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        return sub(a, b, "SafeMath: subtraction overflow");
    }

    










    function sub(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b <= a, errorMessage);
        uint256 c = a - b;

        return c;
    }

    








    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        
        
        
        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }

    










    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        return div(a, b, "SafeMath: division by zero");
    }

    












    function div(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        
        require(b > 0, errorMessage);
        uint256 c = a / b;
        

        return c;
    }

    










    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        return mod(a, b, "SafeMath: modulo by zero");
    }

    












    function mod(uint256 a, uint256 b, string memory errorMessage) internal pure returns (uint256) {
        require(b != 0, errorMessage);
        return a % b;
    }
}

contract Context {
    
    
    constructor () internal { }
    

    function _msgSender() internal view returns (address payable) {
        return msg.sender;
    }

    function _msgData() internal view returns (bytes memory) {
        this; 
        return msg.data;
    }
}

contract Ownable is Context {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    


    constructor () internal {
        _owner = _msgSender();
        emit OwnershipTransferred(address(0), _owner);
    }

    


    function owner() public view returns (address) {
        return _owner;
    }

    


    modifier onlyOwner() {
        require(isOwner(), "Ownable: caller is not the owner");
        _;
    }

    


    function isOwner() public view returns (bool) {
        return _msgSender() == _owner;
    }

    






    function renounceOwnership() public onlyOwner {
        emit OwnershipTransferred(_owner, address(0));
        _owner = address(0);
    }

    



    function transferOwnership(address newOwner) public onlyOwner {
        _transferOwnership(newOwner);
    }

    


    function _transferOwnership(address newOwner) internal {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        emit OwnershipTransferred(_owner, newOwner);
        _owner = newOwner;
    }
}

interface IERC20 {
    


    function totalSupply() external view returns (uint256);

    


    function balanceOf(address account) external view returns (uint256);

    






    function transfer(address recipient, uint256 amount) external returns (bool);

    






    function allowance(address owner, address spender) external view returns (uint256);

    













    function approve(address spender, uint256 amount) external returns (bool);

    








    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    





    event Transfer(address indexed from, address indexed to, uint256 value);

    



    event Approval(address indexed owner, address indexed spender, uint256 value);
}

library Address {
    










    function isContract(address account) internal view returns (bool) {
        
        
        

        
        
        
        bytes32 codehash;
        bytes32 accountHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
        
        assembly { codehash := extcodehash(account) }
        return (codehash != 0x0 && codehash != accountHash);
    }

    





    function toPayable(address account) internal pure returns (address payable) {
        return address(uint160(account));
    }

    

















    function sendValue(address payable recipient, uint256 amount) internal {
        require(address(this).balance >= amount, "Address: insufficient balance");

        
        (bool success, ) = recipient.call.value(amount)("");
        require(success, "Address: unable to send value, recipient may have reverted");
    }
}

library SafeERC20 {
    using SafeMath for uint256;
    using Address for address;

    function safeTransfer(IERC20 token, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transfer.selector, to, value));
    }

    function safeTransferFrom(IERC20 token, address from, address to, uint256 value) internal {
        callOptionalReturn(token, abi.encodeWithSelector(token.transferFrom.selector, from, to, value));
    }

    function safeApprove(IERC20 token, address spender, uint256 value) internal {
        
        
        
        
        require((value == 0) || (token.allowance(address(this), spender) == 0),
            "SafeERC20: approve from non-zero to non-zero allowance"
        );
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, value));
    }

    function safeIncreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).add(value);
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    function safeDecreaseAllowance(IERC20 token, address spender, uint256 value) internal {
        uint256 newAllowance = token.allowance(address(this), spender).sub(value, "SafeERC20: decreased allowance below zero");
        callOptionalReturn(token, abi.encodeWithSelector(token.approve.selector, spender, newAllowance));
    }

    





    function callOptionalReturn(IERC20 token, bytes memory data) private {
        
        

        
        
        
        
        
        require(address(token).isContract(), "SafeERC20: call to non-contract");

        
        (bool success, bytes memory returndata) = address(token).call(data);
        require(success, "SafeERC20: low-level call failed");

        if (returndata.length > 0) { 
            
            require(abi.decode(returndata, (bool)), "SafeERC20: ERC20 operation did not succeed");
        }
    }
}

contract ERC20 is IERC20 {
    using SafeMath for uint256;

    mapping (address => uint256) internal _balances;
    mapping (address => mapping (address => uint256)) internal _allowed;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    uint256 internal _totalSupply;

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowed[owner][spender];
    }

    function transfer(address to, uint256 value) public returns (bool) {
        _transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);
        _transfer(from, to, value);
        return true;
    }

    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0));
        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }
}

contract ERC20Mintable is ERC20 {
    string public name;
    string public symbol;
    uint8 public decimals;

    function _mint(address to, uint256 amount) internal {
        _balances[to] = _balances[to].add(amount);
        _totalSupply = _totalSupply.add(amount);
        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) internal {
        _balances[from] = _balances[from].sub(amount);
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(from, address(0), amount);
    }
}

contract stakingRateModel {
    using SafeMath for *;

    uint256 lastUpdateTimestamp;
    uint256 stakingRateStored;
    uint256 constant ratePerSecond = 21979553177; 
    constructor() public {
        stakingRateStored = 1e18;
        lastUpdateTimestamp = block.timestamp;
    }

    function stakingRate(uint256 time) external returns (uint256 rate) {
        if(time == 30 days) return stakingRateMax().div(12);
        else if(time == 90 days) return stakingRateMax().div(4);
        else if(time == 180 days) return stakingRateMax().div(2);
        else if(time == 360 days) return stakingRateMax();
    }

    function stakingRateMax() public returns (uint256 rate) {
        uint256 timeElapsed = block.timestamp.sub(lastUpdateTimestamp);
        
        if(timeElapsed > 0) {
            lastUpdateTimestamp = block.timestamp;
            rate = timeElapsed.mul(ratePerSecond).add(1e18).mul(stakingRateStored).div(1e18);
            stakingRateStored = rate;
        }
        else rate = stakingRateStored;
    }

}

contract wHakka is Ownable, ERC20Mintable{
    using SafeMath for *;
    using SafeERC20 for IERC20;

    struct vault {
        uint256 hakkaAmount;
        uint256 wAmount;
        uint256 unlockTime;
    }

    event Stake(address indexed holder, address indexed depositor, uint256 amount, uint256 wAmount, uint256 time);
    event Unstake(address indexed holder, address indexed receiver, uint256 amount, uint256 wAmount);

    IERC20 public constant Hakka = IERC20(0x0E29e5AbbB5FD88e28b2d355774e73BD47dE3bcd);
    stakingRateModel public currentModel;

    mapping(address => mapping(uint256 => vault)) public vaults;
    mapping(address => uint256) public vaultCount;
    mapping(address => uint256) public stakedHakka;
    mapping(address => uint256) public votingPower;

    constructor() public {
        symbol = "wHAKKA";
        name = "Wrapped Hakka";
        decimals = 18;
        _balances[address(this)] = uint256(-1);
        _balances[address(0)] = uint256(-1);
    }

    function getStakingRate(uint256 time) public returns (uint256 rate) {
        return currentModel.stakingRate(time);
    }

    function setStakingRateModel(address newModel) external onlyOwner {
        currentModel = stakingRateModel(newModel);
    }


    function stake(address to, uint256 amount, uint256 time) public returns (uint256 wAmount) {
        vault storage v = vaults[to][vaultCount[to]];
        wAmount = getStakingRate(time).mul(amount).div(1e18);
        require(wAmount > 0, "invalid lockup");

        v.hakkaAmount = amount;
        v.wAmount = wAmount;
        v.unlockTime = block.timestamp.add(time);
        
        stakedHakka[to] = stakedHakka[to].add(amount);
        votingPower[to] = votingPower[to].add(wAmount);
        vaultCount[to]++;

        _mint(to, wAmount);
        Hakka.safeTransferFrom(msg.sender, address(this), amount);

        emit Stake(to, msg.sender, amount, wAmount, time);
    }

    
    function unstake(address to, uint256 index, uint256 wAmount) public returns (uint256 amount) {
        vault storage v = vaults[msg.sender][index];
        
        require(block.timestamp >= v.unlockTime, "locked");
        require(wAmount <= v.wAmount, "exceed locked amount");
        amount = wAmount.mul(v.hakkaAmount).div(v.wAmount);

        v.hakkaAmount = v.hakkaAmount.sub(amount);
        v.wAmount = v.wAmount.sub(wAmount);

        stakedHakka[msg.sender] = stakedHakka[msg.sender].sub(amount);
        votingPower[msg.sender] = votingPower[msg.sender].sub(wAmount);

        _burn(msg.sender, wAmount);
        Hakka.safeTransfer(to, amount);
        
        emit Unstake(msg.sender, to, amount, wAmount);
    }

    function inCaseTokenGetsStuckPartial(IERC20 _TokenAddress, uint256 _amount) onlyOwner public {
        require(_TokenAddress != Hakka);
        _TokenAddress.safeTransfer(msg.sender, _amount);
    }

}