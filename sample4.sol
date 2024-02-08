contract Sample {
    function transfer(address _to, uint256 _value) public {
        require(!blacklist[msg.sender]);
        _transfer(msg.sender, _to, _value);
    }

    function ban(address addr) public {
        require(msg.sender == admin);
        blacklist[addr] = true;
    } 

    function enable(address addr) public {
        require(msg.sender == admin);
        blacklist[addr] = false;
    }
 
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(!blacklist[msg.sender]);
        require(_value <= allowance[_from][msg.sender]);     
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public
    returns (bool success) {
        require(!blacklist[msg.sender]);
        allowance[msg.sender][_spender] = _value;
        return true;
    }
}