# agent_vision
## Coloquem outros milestones necessários para finalizar o projeto

- [ ] pedir pro prod Alison avaliar a modularização feita nessa implementação

- [ ] criar arquivo de motion.py

- [ ] testar o robô com o arquivo motion.py (atualmente o código não está modularizado como esse)

- [ ] chamar cython para partes do codigo que puderem compiladas em c (código otimizado)

- [ ] testar aquisição de imagem com câmera normal, abandonar o esp32-cam para diminuir overhead da transmissão de imagem por http

```mermaid
flowchart TD
    A(Início: Executa main.py) --> B(Inicializa o objeto Agent)
    B --> C(Define biblioteca de planos com posições e ações)
    C --> D(Abre a câmera para captura de vídeo)
    D --> E{Câmera aberta?}
    E -- Não --> F(Exibe erro e encerra)
    E -- Sim --> G(Loop principal: leitura dos frames)
    G --> H(Captura um frame da webcam)
    H --> I(Detecta posição do rosto)
    I -- Rosto detectado --> J(Atualiza crença da posição)
    I -- Nenhum rosto --> K(Continua sem atualizar crenças)
    J --> L(Adiciona desejo de ajustar visão)
    L --> M(Obtém plano correspondente)
    M -- Plano encontrado --> N(Define intenção e adiciona ações)
    M -- Nenhum plano --> O(Não executa ações)
    N --> P(Executa ações para ajustar a visão)
    P --> G(Volta ao loop para novo frame)
    O --> G(Volta ao loop para novo frame)
    G -- Tecla 'q' pressionada? --> Q{Sim}
    Q --> R(Finaliza execução)
```