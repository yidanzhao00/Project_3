contract Portfolio {
    // The asset structure
    struct Asset {
        address creator;
        uint id;  // 6 bytes string
        int price;
        int quantity;
    }

    // Counts
    int asset_count;

    // Lists
    mapping (int => Asset) assets;

    // private functions

    // Events
    event AssetJoined(address indexed asset_address, int index, uint id, int quantity, int price, uint256 timestamp);
    event AssetUpdated(address indexed asset_address, int index, uint id, int quantity, int price, uint256 timestamp);
    
    function addAsset(uint _id, int _quantity, int _price) public payable returns (bool success) {
        int asset_index = getAssetIndex(_id);
        if(asset_index == -1){
            asset_count = asset_count + 1;
            Asset memory _asset = Asset(msg.sender, _id, _price, _quantity); 
            assets[asset_count] = _asset;
            emit AssetJoined(msg.sender,asset_count,  _id, _quantity, _price, now);
        } else {
            assets[asset_index].quantity = _quantity; 
            assets[asset_index].price = _price;
            emit AssetUpdated(msg.sender, asset_index, _id, _quantity, _price, now);
        }

        return true;
    }
    
    // Gets an asset index in the mapping by id
    function getAssetIndex(uint _id) public view returns (int index) {
        for (int i = 1; i <= asset_count; i++) {
         return i;
        } 
    }
  