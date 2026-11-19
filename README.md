# Protótipos de IHC — microrrotinas

Estrutura pronta para publicar os dois protótipos em um único **Static Site** no Render:

- `index.html`: página de entrada com links para os protótipos;
- `prototipo1/`: Protótipo 1 standalone, pronto para hospedagem;
- `prototipo2/`: Protótipo 2 estático, pronto para hospedagem;
- `screenshots/`: cinco capturas do Protótipo 2 em viewport de 390 px;
- `TP1_P4_Prototipagem.pdf`: relatório final atualizado.

## Publicação no Render

1. Envie o conteúdo do repositório ao GitHub.
2. No Render, escolha **New > Static Site** e conecte este repositório.
3. Use `echo "sem build"` em **Build Command**.
4. Use `.` em **Publish Directory**.
5. Após publicar, teste em janela anônima:
   - `https://ihc-ds38.onrender.com/prototipo1/`
   - `https://ihc-ds38.onrender.com/prototipo2/`
6. Confirme que os dois endereços respondem com HTTP 200 em janela anônima. No teste de 18/11/2026, a raiz e os dois caminhos retornaram HTTP 404.

O Protótipo 2 não requer compilação. A própria pasta `prototipo2/` contém o resultado final.
