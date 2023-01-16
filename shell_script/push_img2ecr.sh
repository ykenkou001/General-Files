#!/bin/bash

read -p "input profile name! " str

aws_account_id=`aws sts get-caller-identity --query 'Account' --output text --profile="$str"`
echo aws_account_id: $aws_account_id

select var in login create_repo RepositoryList Usage 

do
	# ecrにログイン
    if [ "$var" == "login" ];then
    	aws ecr get-login-password --region ap-northeast-1 --profile "$str" |\
				docker login --username AWS --password-stdin \
				"$aws_account_id".dkr.ecr.ap-northeast-1.amazonaws.com
	# repositoryの作成
	elif [ "$var" == "create_repo" ];then
		read -p "input repository name! " r_name
    	# $r_nameにrepository-nameが必要
	    aws ecr create-repository \
	    --repository-name "$r_name" \
	    --image-scanning-configuration scanOnPush=true \
	    --region ap-northeast-1 \
	    --profile "$str"
	# repository一覧
	elif [ "$var" == "RepositoryList" ];then
		echo ------ Repository List -------
		aws ecr describe-repositories --output json --profile "$str" | jq -re ".repositories[].repositoryName"
	# usage
	elif [ "$var" == "Usage" ];then
        echo "Usage: login | create_repo"
    fi
    break
done
