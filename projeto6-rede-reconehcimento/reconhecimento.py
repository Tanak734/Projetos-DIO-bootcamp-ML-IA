import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import cv2
import numpy as np
import os
from PIL import Image
import time

# Configurações
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
IMG_SIZE = 100
NUM_CLASSES = 2  # Duas classes: homem e mulher
DATA_PATH = r'C:\Users\Felip\Code\estudo\Machine_Learning_IA\bootcamp-dio\Projetos_BOOTCAMP_DIo\projeto6-rede-reconehcimento\dataset'
BATCH_SIZE = 8
EPOCHS = 10

# Criar diretório para dados
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, 'homem'), exist_ok=True)
os.makedirs(os.path.join(DATA_PATH, 'mulher'), exist_ok=True)

# Pré-processamento das imagens
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Classe para dataset customizado
class GenderDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Mapear nomes para IDs (0 para homem, 1 para mulher)
        self.class_to_id = {'homem': 0, 'mulher': 1}
        
        for class_name in os.listdir(data_path):
            class_path = os.path.join(data_path, class_name)
            if os.path.isdir(class_path):
                for img_name in os.listdir(class_path):
                    if img_name.endswith('.jpg') or img_name.endswith('.png'):
                        self.images.append(os.path.join(class_path, img_name))
                        self.labels.append(self.class_to_id[class_name])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = Image.open(self.images[idx]).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]

# Definir a arquitetura da CNN
class GenderCNN(nn.Module):
    def __init__(self, num_classes):
        super(GenderCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 16 * 16, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 16 * 16)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# Coletar dados
def collect_data():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("Coletando dados para treinamento...")
    print("Pressione 'h' para capturar imagem de homem, 'm' para mulher, 'q' para sair")
    
    count_homem = 0
    count_mulher = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        
        cv2.putText(frame, f"Homens: {count_homem}, Mulheres: {count_mulher}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Pressione 'h' para homem, 'm' para mulher, 'q' para sair", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Coletando Dados', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('h') and len(faces) > 0:
            # Salvar imagem de homem
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(DATA_PATH, 'homem', f'{count_homem}.jpg'), face_img)
                count_homem += 1
                print(f"Capturada imagem de homem: {count_homem}")
            break
            
        elif key == ord('m') and len(faces) > 0:
            # Salvar imagem de mulher
            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(DATA_PATH, 'mulher', f'{count_mulher}.jpg'), face_img)
                count_mulher += 1
                print(f"Capturada imagem de mulher: {count_mulher}")
            break
            
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Coleta de dados concluída!")

# Treinar o modelo
def train_model():
    # Verificar se há dados para treinamento
    if not os.listdir(DATA_PATH):
        print("Nenhum dado encontrado. Execute a coleta de dados primeiro.")
        return
    
    dataset = GenderDataset(DATA_PATH, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    model = GenderCNN(NUM_CLASSES).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print("Iniciando treinamento...")
    
    for epoch in range(EPOCHS):
        for batch_idx, (data, targets) in enumerate(dataloader):
            data = data.to(DEVICE)
            targets = targets.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
        print(f'Epoch {epoch+1}/{EPOCHS}, Loss: {loss.item():.4f}')
    
    # Salvar modelo
    torch.save(model.state_dict(), 'gender_model.pth')
    print("Modelo treinado e salvo!")

# Reconhecimento em tempo real
def real_time_recognition():
    # Verificar se o modelo existe
    if not os.path.exists('gender_model.pth'):
        print("Modelo não encontrado. Execute o treinamento primeiro.")
        return
    
    # Carregar modelo
    model = GenderCNN(NUM_CLASSES).to(DEVICE)
    model.load_state_dict(torch.load('gender_model.pth', map_location=DEVICE))
    model.eval()
    
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("Iniciando reconhecimento de gênero. Pressione 'q' para sair.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
            input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE)
            
            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                confidence, prediction = torch.max(probabilities, 0)
                
            gender = "Homem" if prediction.item() == 0 else "Mulher"
            color = (255, 0, 0) if prediction.item() == 0 else (0, 0, 255)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            label = f"{gender}: {confidence:.2f}"
            cv2.putText(frame, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.imshow('Reconhecimento de Gênero', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Executar o fluxo completo
if __name__ == "__main__":
    print("=== Sistema de Reconhecimento de Gênero ===")
    
    while True:
        print("\nOpções:")
        print("1. Coletar dados")
        print("2. Treinar modelo")
        print("3. Reconhecimento em tempo real")
        print("4. Sair")
        
        choice = input("Escolha uma opção (1-4): ")
        
        if choice == '1':
            collect_data()
        elif choice == '2':
            train_model()
        elif choice == '3':
            real_time_recognition()
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")