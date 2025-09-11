import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = r'dataset' # coloque o dataset aqui
IMG_SIZE = (224, 224)
TOP_K = 4

model = VGG16(weights='imagenet', include_top=False, pooling='avg')

def load_and_preprocess(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Imagem não pode ser carregada: {img_path}")
    img = cv2.resize(img, IMG_SIZE)
    img = preprocess_input(img)
    return img

def load_all_images(directory):
    image_paths = []
    features = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                try:
                    img = load_and_preprocess(img_path)
                    img_batch = np.expand_dims(img, axis=0)
                    feature = model.predict(img_batch, verbose=0).flatten()
                    image_paths.append(img_path)
                    features.append(feature)
                except Exception as e:
                    print(f"Erro ao processar {img_path}: {e}")
    
    return image_paths, np.array(features)

def find_similar_images(query_idx, features, top_k=TOP_K):
    query_feature = features[query_idx]
    similarities = cosine_similarity([query_feature], features)[0]
    
    sorted_indices = np.argsort(similarities)[::-1]
    similar_indices = [idx for idx in sorted_indices if idx != query_idx][:top_k]
    similar_scores = similarities[similar_indices]
    
    return similar_indices, similar_scores

def display_results(query_path, similar_paths, similarity_scores):
    query_img = cv2.cvtColor(cv2.imread(query_path), cv2.COLOR_BGR2RGB)
    similar_imgs = [cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB) for path in similar_paths]
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, TOP_K + 1, 1)
    plt.imshow(query_img)
    plt.title('Imagem de Consulta')
    plt.axis('off')
    
    for i, (img, score) in enumerate(zip(similar_imgs, similarity_scores)):
        plt.subplot(1, TOP_K + 1, i + 2)
        plt.imshow(img)
        plt.title(f'Similar {i+1}\n({score:.3f})')
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Diretório {DATA_DIR} não encontrado!")
        print("Crie a estrutura: dados/{cadeiras,produtos_eletronicos,relogios,cervejas}/")
        exit()
    
    print("Carregando e processando imagens...")
    image_paths, features = load_all_images(DATA_DIR)
    
    if not image_paths:
        print("Nenhuma imagem encontrada. Verifique o diretório.")
        exit()
    
    print(f"Processadas {len(image_paths)} imagens.")
    
    query_idx = np.random.randint(0, len(image_paths))
    query_path = image_paths[query_idx]
    print(f"Imagem de consulta: {query_path}")
    
    similar_indices, similarity_scores = find_similar_images(query_idx, features)
    
    similar_paths = [image_paths[i] for i in similar_indices]
    
    display_results(query_path, similar_paths, similarity_scores)
    
    print("\nImagens recomendadas:")
    for i, (path, score) in enumerate(zip(similar_paths, similarity_scores)):
        print(f"{i+1}. {path} (similaridade: {score:.3f})")