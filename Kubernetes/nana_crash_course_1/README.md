# Kubernetes Crash Course: Hands-On Tutorial

## Overview
This README provides an outline and summary of the "Hands-On Kubernetes Tutorial | Learn Kubernetes in 1 Hour - Kubernetes Course for Beginners" by TechWorld with Nana. The video is a comprehensive crash course on Kubernetes (K8s), covering core concepts, architecture, components, setup, and a practical demo project. 

- **Video Link**: [Watch on YouTube](https://www.youtube.com/watch?v=s_o8dwzRlu4&t=3913s)
- **Duration**: ~1 hour
- **Instructor**: Nana from TechWorld with Nana
- **Published**: September 30, 2021
- **Key Topics**: Kubernetes basics, architecture, components, local setup with Minikube, and deploying a web app with MongoDB.
- **Target Audience**: Beginners in Kubernetes, DevOps enthusiasts.

This course assumes basic knowledge of Docker and YAML. If needed, check the prerequisites section below.

## Course Objectives
By the end of this course, you'll:
- Understand what Kubernetes is and why it's used.
- Learn Kubernetes architecture and key components.
- Set up a local Kubernetes cluster using Minikube and kubectl.
- Deploy a full-stack application (WebApp + MongoDB) with configurations like ConfigMaps, Secrets, Deployments, and Services.
- Interact with and troubleshoot your Kubernetes cluster.

## Table of Contents
Based on the video timestamps and sections:

1. **Intro and Course Overview** (0:00)
   - Welcome and what you'll learn.

2. **What is Kubernetes** (1:44)
   - Definition: Open-source container orchestration platform.
   - Problems it solves: Managing microservices, scalability, high availability, disaster recovery.
   - Rise of containers and need for orchestration.

3. **Kubernetes Architecture** (4:33)
   - Master node components: API Server, Controller Manager, Scheduler, etcd.
   - Worker nodes: Kubelet, Pods, Containers.
   - Virtual network for inter-node communication.
   - High availability with multiple masters.

4. **Main Kubernetes Components** (8:58)
   - **Node & Pod** (9:29): Basic units; Pods as abstractions over containers.
   - **Service & Ingress** (12:19): Services for stable IPs and load balancing; Ingress for external access with domain names.
   - **ConfigMap & Secret** (14:31): External configuration; Secrets for sensitive data (base64 encoded).
   - **Volume** (17:52): Persistent storage for data beyond pod lifecycles.
   - **Deployment & StatefulSet** (19:46): Blueprints for stateless apps (Deployment) and stateful apps (StatefulSet) with replicas.

5. **Kubernetes Configuration** (26:28)
   - YAML files for defining components.
   - Syntax for Pods, Services, Deployments, etc.

6. **Minikube and Kubectl - Setup K8s Cluster Locally** (32:39)
   - Install Minikube (local K8s cluster) and kubectl (CLI tool).
   - Commands: `minikube start`, `kubectl get nodes`.

7. **Complete Demo Project: Deploy WebApp with MongoDB** (41:17)
   - Project overview: Node.js web app connected to MongoDB.
   - Create ConfigMap for DB URL.
   - Create Secret for DB credentials.
   - MongoDB Deployment and Service.
   - WebApp Deployment and Service (with NodePort for external access).
   - Pass data via environment variables.
   - Deploy resources: `kubectl apply -f <file.yaml>`.
   - Validate: Access app in browser via Minikube IP and NodePort.

8. **Interacting with Kubernetes Cluster** (1:05:40)
   - Commands: `kubectl get all`, `kubectl describe <resource>`, `kubectl logs <pod>`.
   - Troubleshooting and logs.

9. **Conclusion** (1:11:03)
   - Recap and next steps.

## Prerequisites
- **Docker**: Basic understanding. [Learn Docker here](https://youtu.be/3c-iBn73dDE).
- **YAML**: Syntax basics. [Learn YAML here](https://youtu.be/1uFVr15xDGg).
- Install Minikube: Follow [official guides](https://minikube.sigs.k8s.io/docs/start/).
- Install kubectl: Comes with Minikube or install separately.

## Resources and Links
- **Git Repo for Demo**: [gitlab.com/nanuchi/k8s-in-1-hour](https://gitlab.com/nanuchi/k8s-in-1-hour)
- **Minikube Docs**: [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)
- **Kubernetes Official Docs**: [kubernetes.io](https://kubernetes.io/docs/home/)
- **Sponsor**: Kasten (Kubernetes backup tool) - [kasten.io/nana](https://www.kasten.io/nana)
- **Related Courses**:
  - Full Kubernetes Course (4 hours): [YouTube](https://youtu.be/X48VuDVv0do)
  - Become a Kubernetes Administrator (CKA): [bit.ly/3Iwn71q](https://bit.ly/3Iwn71q)
  - Complete DevOps Bootcamp: [bit.ly/3MQgadT](https://bit.ly/3MQgadT)
- **DevOps Roadmap**: [bit.ly/44xBHBD](https://bit.ly/44xBHBD)

## Hands-On Practice
Follow along with the demo:
1. Clone the repo: `git clone https://gitlab.com/nanuchi/k8s-in-1-hour.git`
2. Start Minikube: `minikube start`
3. Apply configs: `kubectl apply -f mongo-config.yaml`, etc.
4. Access app: `minikube ip` + NodePort (e.g., http://192.168.99.100:30100)
5. Clean up: `kubectl delete -f <file.yaml>`, `minikube stop`

## Differences from Previous Course
This is a shorter, updated version of the 4-hour K8s course with new animations, Minikube installation updates, and a fresh demo project.

## Connect with the Instructor
- YouTube: [TechWorld with Nana](https://www.youtube.com/channel/UCdngmbVKX1Tgre699-XLlUA)
- Instagram: [instagram.com/techworld_with_nana](https://bit.ly/2F3LXYJ)
- Twitter: [twitter.com/techworld_nana](https://bit.ly/3i54PUB)
- LinkedIn: [linkedin.com/in/nana-janashia](https://bit.ly/3hWOLVT)

If you found this course helpful, like, subscribe, and share! For advanced learning, check the related courses.