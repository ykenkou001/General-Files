#!/bin/zsh

# set aws profile
PROFILE=aoz

# Define Function
function get_instance_info() {
    aws ec2 describe-instances \
    --filters "Name=tag:name,Values=yamashita" \
    --profile $PROFILE \
    --query 'Reservations[*].Instances[*].'[$1]'' | jq -r '.[][][]'
}

IDS=`get_instance_info InstanceId`
# echo IDS: $IDS
DNS=`get_instance_info PublicDnsName`

OBJECTIVE=(Infos status start stop terminate connect \
Transfer_local_file_to_ec2 reboot Transfer_file_in_ec2_to_local \
Transfer_local_directory_to_ec2)

# Get instance name: yamashta-devのinstance ids
INFOS=(InstanceId ImageId Keyname InstanceType \
PublicIpAddress PublicDnsName State.Name exit)

select obj in ${OBJECTIVE[@]}
do
    # インスタンスの状態の確認
    if [ "$obj" == "Infos" ]
    then
        echo "what you want to know about ec2 instance?"
        select info in ${INFOS[@]}
        do
            if [ "$info" == "exit" ]
            then
                break
            else
                echo $info: `get_instance_info $info`
            fi
        done
        break
    elif [ "$obj" == "status" ]
    then
        echo `get_instance_info State.Name`
        break
    # instanceを開始する
    elif [ "$obj" == "start" ]
    then
        aws ec2 start-instances --instance-ids $IDS --profile $PROFILE
        break
    # instanceを停止する
    elif [ "$obj" == "stop" ]
    then
        aws ec2 stop-instances --instance-ids $IDS --profile $PROFILE
        break
    # instanceの終了
    elif [ "$obj" == "terminate" ]
    then
        aws ec2 terminate-instances --instance-ids $IDS --profile $PROFILE
        break
    # instanceに接続する
    elif [ "$obj" == "connect" ]
    then
        ssh -i "~/.ssh/yamashita-rsa.pem" ec2-user@$DNS
        break
    elif [ "$obj" == "Transfer_local_file_to_ec2" ]
    then
        read -e -p "input local file path > " file_path
        read -e -p "input remote directory path > " remote_path
        # ローカルの任意のファイル($2: file path)をインスタンスに転送 -> :/home/ec2-user/
        scp -i ~/.ssh/yamashita-rsa.pem $file_path ec2-user@$DNS:$remote_path
        break
    # instanceの再起動
    elif [ "$obj" == "reboot" ]
    then
        aws ec2 reboot-instances --instance-ids $IDS --profile $PROFILE
        break
    elif [ "$obj" == "Transfer_file_in_ec2_to_local" ]
    then
        # インスタンスから任意のファイル($2: file path)をローカル($3)に転送
        # $2: file path in ec2, $3: local file path
        read -e -p "input file path in ec2 > " file_path_in_ec2
        read -e -p "input directory path in local > " dir_path_in_local
        scp -i ~/.ssh/yamashita-rsa.pem ec2-user@$DNS:$file_path_in_ec2 $dir_path_in_local
        break
    elif [ "$obj" == "Transfer_local_directory_to_ec2" ]
    then
        # ローカルの任意ディレクトリ($2: directory path)をインスタンスに転送 -> :/home/ec2-user/
        read -e -p "input directory path in local > " dir_path_in_local
        read -e -p "targe dir path in ec2 > " target_dir_in_ec2
        scp -i ~/.ssh/yamashita-rsa.pem -r $dir_path_in_local ec2-user@$DNS:$target_dir_in_ec2
        break
    else
        echo "Please select one of the following options."
        echo "Infos, \nstatus \nstart \nstop \nterminate \nconnect \
\nTransfer_files_to_ec2 \nreboot \nTransfer_files_locally_from_ec2 \
\nTransfer_local_directory_to_ec2"
        break
    fi
done

