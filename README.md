# LabCore — revisão para o seu repositório

Esta versão corrige o projeto `isa01254/labcore` e usa as **capturas PNG originais** de `static/assets`. O novo jogo apresenta um laboratório, personagem animado, cinco missões científicas, equipamentos clicáveis, perguntas com imagens ampliáveis, pontos, estrelas, desbloqueio de fases, cadastro, perfil e ranking.

## Instalação recomendada (aproveita TODAS as imagens e seus usuários)

1. Faça uma cópia de segurança da pasta `labcore` no seu computador. **Não apague `static/assets` nem `db.sqlite3`**.
2. Extraia o ZIP desta revisão em uma pasta temporária, por exemplo `Downloads\LabCore_Atualizado`.
3. Dê dois cliques em `APLICAR_NO_REPO.bat`, informe o caminho completo da pasta original `labcore` e aguarde o backup/instalação. Se preferir o terminal, execute:

   ```powershell
   py -3 INSTALAR_NO_REPO.py "C:\Users\SEU_USUARIO\labcore"
   ```

   Esse comando copia os arquivos revisados, faz backup dos arquivos substituídos e **preserva todas as imagens originais, o banco de dados, o ambiente virtual e a pasta `.git`**.
4. Abra a pasta `labcore` original no VS Code e execute `INICIAR_LABCORE.bat`. Você também pode executar `python main.py`. O jogo abrirá em `http://127.0.0.1:8000/`.

**Se preferir:** extraia diretamente o conteúdo do ZIP dentro da pasta original `labcore`, aceite substituir os arquivos de código e **mantenha a pasta `static/assets` original**. Neste caso, faça backup antes e não precisa executar `INSTALAR_NO_REPO.py`.

### Sobre o erro `No module named whitenoise`

A configuração local foi corrigida e **não exige WhiteNoise**. `INICIAR_LABCORE.bat` usa o Python da `.venv`, instalando o Django se necessário. Não precisa executar `Activate.ps1` nem alterar a política de execução do PowerShell.

### Imagens

A versão anterior interrompia a abertura se a internet estivesse sem acesso ao GitHub. Nesta revisão, **nenhum download é obrigatório na abertura**. As PNGs originais são aproveitadas da sua cópia do repositório. Se faltar alguma, o jogo continua jogável, mostra um aviso e usa um desenho de reserva apenas naquele lugar. Para conferir: `python verificar_imagens.py`.

**Atenção:** este ZIP contém o código completo e um pequeno ícone SVG de apoio; **não duplica as PNGs do repositório original**. Instale sobre sua cópia original para ter imediatamente todas as imagens sem precisar de internet.

### Controles e funcionamento

No mapa, abra uma fase desbloqueada. Ande com W/A/S/D ou as setas; `E` interage com o equipamento mais próximo. Também é possível **clicar ou tocar diretamente nas imagens dos equipamentos**. Clique na imagem da pergunta para ampliar e escolha uma resposta. Após acerto, o equipamento ganha indicação verde de concluído. Respostas e fases já pontuadas não geram XP repetido. `Esc` volta para o mapa; no celular use os controles na tela.

### Testes

Os testes do navegador e da estrutura podem ser executados com `python -m unittest discover -s tests -v` (testes de estrutura) e `python main.py test labcore_game` (testes do Django). Para depurar o cliente JavaScript, use o console do navegador (F12). Esta entrega foi testada em navegador isolado; o Django não pôde ser instalado no ambiente de desenvolvimento desta revisão por indisponibilidade de rede, portanto execute o comando Django no seu computador para conferir o backend.

O repositório conectado está em modo **somente leitura** nesta conversa; esta revisão não foi publicada automaticamente na branch `main` do GitHub.
