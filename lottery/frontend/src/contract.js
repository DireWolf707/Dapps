export let abi = [{'inputs': [{'internalType': 'address', 'name': '_priceFeed', 'type': 'address'}, {'internalType': 'address', 'name': '_vrf', 'type': 'address'}, {'internalType': 'address', 'name': '_link', 'type': 'address'}, {'internalType': 'bytes32', 'name': '_keyHash', 'type': 'bytes32'}, {'internalType': 'uint256', 'name': '_fee', 'type': 'uint256'}], 'stateMutability': 'nonpayable', 'type': 'constructor', 'name': 'constructor'}, {'anonymous': false, 'inputs': [{'indexed': true, 'internalType': 'address', 'name': 'previousOwner', 'type': 'address'}, {'indexed': true, 'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'OwnershipTransferred', 'type': 'event'}, {'anonymous': false, 'inputs': [{'indexed': false, 'internalType': 'bytes32', 'name': 'requestId', 'type': 'bytes32'}], 'name': 'RequestRandomness', 'type': 'event'}, {'inputs': [], 'name': 'endLottery', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'enter', 'outputs': [], 'stateMutability': 'payable', 'type': 'function'}, {'inputs': [], 'name': 'getEntranceFee', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getPlayers', 'outputs': [{'internalType': 'address[]', 'name': '', 'type': 'address[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'getPrice', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'isOwner', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'lastWinner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'lottery_state', 'outputs': [{'internalType': 'enum Lottery.LOTTERY_STATE', 'name': '', 'type': 'uint8'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'owner', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'name': 'playerEntered', 'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'players', 'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'priceFeed', 'outputs': [{'internalType': 'contract AggregatorV3Interface', 'name': '', 'type': 'address'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'bytes32', 'name': 'requestId', 'type': 'bytes32'}, {'internalType': 'uint256', 'name': 'randomness', 'type': 'uint256'}], 'name': 'rawFulfillRandomness', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'renounceOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'startLottery', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': 'newOwner', 'type': 'address'}], 'name': 'transferOwnership', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [], 'name': 'usdEntryFee', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}];export let address = '0x458679Cf29825aEB12DB16631FF0B34abB949Ed4';