Gas Me Up is a tool to simplify gas reimbursements for DAOs.

You will need to set the following environment variables:
 - $ETHERSCAN_TOKEN

To use this tool as a contributor:
 1. Copy the my_details_TEMPLATE.py file
 2. Rename your copy to my_details.py
 3. Specify your address(es) in the 'my_addresses' list in my_details.py
    (ENS domain names will work)
 4. Set the 'handle' variable in my_details.py to your publicly known handle
 5. If you only use these addresses for your DAO-related work, set the 'skip_confirm' veriable in my_details.py to 'True'
 6. Open a terminal and type 'brownie run gasmeup'
 7. If 'skip_confirm' is 'False', progress through the prompts to confirm each tx was made for DAO-purposes and is reimbursable
 8. Submit a PR to master



