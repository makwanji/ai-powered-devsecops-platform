#!/bin/bash

# disable firewalld
sudo systemctl disable --now firewalld

# Install K3s
# curl -sfL https://get.k3s.io | sh -
# curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --node-ip=10.21.209.72 --advertise-address=10.21.209.72 --bind-address=10.21.209.72 --flannel-iface=$(ip route get 10.21.209.72 | awk '{print $3; exit}')" sh -
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v1.34.8+k3s1" sh -


sudo systemctl status k3s
sudo k3s kubectl get nodes

# Set up kubectl for your user
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config
echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc

kubectl get nodes
kubectl get pods -A

# Find your VM's IP
hostname -I


# deploy Sample application

kubectl apply -f demoapps/deployment.yaml
kubectl apply -f demoapps/service.yaml
kubectl apply -f demoapps/ingress.yaml
