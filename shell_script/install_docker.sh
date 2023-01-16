#!/bin/bash
if [ "$1" == "install_docker" ]
then
    # インスタンスでinstallされているパッケージとパッケージキャッシュを更新
    sudo yum update -y
    # Docker Comunity Editionパッケージをインストール
    sudo amazon-linux-extras install docker
    # Dockerサービスを起動
    sudo service docker start
    # ec2-userでdockerコマンドを実行するためにsudoを付与
    sudo usermod -a -G docker ec2-user
    echo "sudoなしでDockerコマンドを実行できることを確認"
    docker info

elif [ "$1" == "reboot" ]
then
    sudo shutdown -r now

else
    echo "Usage: $0 install_docker | reboot"
fi
