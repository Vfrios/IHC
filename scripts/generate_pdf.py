from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'TP1_P4_Prototipagem.pdf'
font='Arial'
for regular,bold in [(Path('C:/Windows/Fonts/arial.ttf'),Path('C:/Windows/Fonts/arialbd.ttf'))]:
    if regular.exists():
        pdfmetrics.registerFont(TTFont('Arial',str(regular))); pdfmetrics.registerFont(TTFont('Arial-Bold',str(bold)))
    else: font='Helvetica'
bold=font+'-Bold' if font=='Arial' else 'Helvetica-Bold'
styles=getSampleStyleSheet()
body=ParagraphStyle('Body',fontName=font,fontSize=8.5,leading=11.2,textColor=colors.HexColor('#222222'),spaceAfter=5)
small=ParagraphStyle('Small',parent=body,fontSize=7.2,leading=9)
h1=ParagraphStyle('H1',fontName=bold,fontSize=16,leading=19,spaceBefore=8,spaceAfter=9,textColor=colors.HexColor('#111111'))
h2=ParagraphStyle('H2',fontName=bold,fontSize=12,leading=14,spaceBefore=8,spaceAfter=6)
title=ParagraphStyle('Title',fontName=bold,fontSize=17,leading=21,alignment=TA_CENTER,spaceAfter=14)
caption=ParagraphStyle('Caption',fontName=font,fontSize=7.5,leading=9,alignment=TA_CENTER,spaceBefore=3)
cell=ParagraphStyle('Cell',fontName=font,fontSize=6.7,leading=8.2)
cellb=ParagraphStyle('CellB',parent=cell,fontName=bold)

def P(x,s=body): return Paragraph(x,s)
def header_footer(canvas,doc):
    canvas.saveState(); w,h=A4
    canvas.setFont(font,7.5); canvas.setFillColor(colors.HexColor('#333333'))
    canvas.drawString(1.5*cm,h-1.0*cm,'TP1 · Parte 4: Geração do Protótipo · PUC Minas · Interação Humano Computador')
    canvas.drawRightString(w-1.5*cm,h-1.0*cm,f'Página {doc.page}')
    canvas.setStrokeColor(colors.HexColor('#b9b9b9')); canvas.line(1.5*cm,h-1.18*cm,w-1.5*cm,h-1.18*cm)
    canvas.restoreState()
def table(data,widths,header=True,fs=cell):
    cooked=[[v if hasattr(v,'wrap') else P(str(v),cellb if header and r==0 else fs) for v in row] for r,row in enumerate(data)]
    t=Table(cooked,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
    cmds=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#9f9f9f')),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]
    if header: cmds += [('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e9ece9')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#111111'))]
    t.setStyle(TableStyle(cmds)); return t
def fitted_image(path,max_width=5.0*cm,max_height=10.7*cm):
    with PILImage.open(path) as src:
        width,height=src.size
    scale=min(max_width/width,max_height/height)
    return Image(str(path),width=width*scale,height=height*scale)

story=[]
story += [Spacer(1,.25*cm),P('Pontifícia Universidade Católica de Minas Gerais',ParagraphStyle('uni',parent=body,fontName=bold,fontSize=11,alignment=TA_CENTER)),P('Instituto de Ciências Exatas e Informática (ICEI)<br/>Engenharia de Software<br/>Disciplina: Interação Humano Computador<br/>Professora: Joana Gabriela Ribeiro de Souza',ParagraphStyle('meta',parent=body,alignment=TA_CENTER,leading=13)),Spacer(1,.15*cm),P('<b>Integrantes do grupo (ordem alfabética):</b> Brayan Mendes de Carvalho; Joao Vitor Soares; Michael William Tang; Vitor de Freitas Rios.',body),Spacer(1,.2*cm),P('TRABALHO PRÁTICO 1 – PARTE 4:<br/>GERAÇÃO DO PROTÓTIPO',title),P('1. Requisitos do software',h1),P('Requisitos derivados das evidências da Parte 2 e da modelagem de tarefas da Parte 3. RF = requisito funcional; RNF = requisito não funcional.',body)]
reqs=[
('RF01','Cadastrar curso, vínculo e carga horária.','Rotina varia por vínculo e carga.','HTA 1.1 · MoLIC Cena 1'),('RF02','Informar e atualizar janelas de tempo livre.','Tempo fragmentado em pequenos intervalos.','HTA 1.2 · Cenas 1 e 2'),('RF03','Definir local e duração preferida.','Flexibilidade determina a consistência.','HTA 1.3 · Cena 1'),('RF04','Definir objetivo pessoal.','Aliviar estresse e melhorar disposição.','HTA 1.4'),('RF05','Sugerir microrrotina conforme tempo e local.','Mínimo esforço de decisão.','HTA 2.1–2.3 · Cena 2'),('RF06','Aceitar, trocar ou ajustar a sugestão.','Adaptação a dias atípicos.','HTA 2.4 · Cena 2'),('RF07','Treino guiado com iniciar, pular e pausar.','Orientação sem planejamento adicional.','HTA 3.1–3.2 · Cena 3'),('RF08','Registrar conclusão total ou parcial sem punição.','Evitar culpa e abandono.','HTA 3.3 · Cena 3'),('RF09','Exibir feedback ao concluir.','Reforço positivo do progresso.','HTA 3.4 · Cena 3'),('RF10','Modo Sobrecarga com 5 a 10 min/dia.','Preservar o hábito em semanas de prova.','HTA 4.1–4.3 · Cena 4'),('RF11','Mostrar histórico e sequência.','Motivação pelo progresso acumulado.','HTA 5.1 · Cena 5'),('RF12','Reforço e lembretes gentis.','Evitar sentimento de fracasso.','HTA 5.2 · Cenas 2 e 5'),('RF13','Ajustar metas sob demanda.','Metas irreais causam desânimo.','HTA 5.3 · Cena 5'),('RF14','Salvar e retomar a configuração.','Interrupções são comuns na rotina.','MoLIC Cena 1'),('RNF01','Configuração inicial em menos de 2 min.','Baixo esforço cognitivo.','MoLIC Cena 1'),('RNF02','Iniciar treino em até 3 interações da Home.','Reduzir desistência.','HTA 2 e 3'),('RNF03','Mensagens acolhedoras, sem culpa.','Metamensagem do sistema.','Todas as falhas'),('RNF04','Contraste, legibilidade e alvos amplos.','Uso cansado e em movimento.','Todas as cenas'),('RNF05','Interface responsiva e mobile-first.','Uso em pequenos intervalos.','Todas as cenas'),('RNF06','Resposta imediata.','Janelas curtas não comportam espera.','HTA 2 e 3'),('RNF07','Dados restritos ao usuário.','Dados pessoais e de rotina.','HTA 1'),('RNF08','Consistência visual e de navegação.','Reduzir carga cognitiva.','Todas as cenas')]
story.append(table([('ID','Descrição','Justificativa / necessidade','Relação com Etapa 3')]+reqs,[1.2*cm,7.1*cm,5.0*cm,3.7*cm]))
story += [PageBreak(),P('2. Ferramentas utilizadas',h1),P('Foram utilizadas duas ferramentas de IA distintas, com o mesmo conjunto de requisitos e orientações gerais, para permitir comparação justa.',body)]
tools=[('Ferramenta','Como foi empregada'),('Ferramenta 1: Claude (Anthropic, modelo Claude Sonnet 5.5, via claude.ai)','Recebeu o prompt e gerou uma aplicação React/Vite. A versão standalone entregue em prototipo1/ foi mantida sem alteração funcional e seu fluxo foi testado no navegador.'),('Ferramenta 2: OpenAI Codex, modelo GPT-5, no ambiente Codex (plano da conta não é exibido pelo ambiente)','Recebeu o prompt integral em uma geração e criou o EntrePausas em HTML/CSS/JavaScript. Não houve ajuste funcional posterior na primeira versão mantida em prototipo2/. O fluxo foi testado de ponta a ponta e preparado para hospedagem.')]
story += [table(tools,[5.4*cm,11.6*cm]),P('3. Processo de geração',h1),P('<b>Prompt-base:</b> criação de protótipo web interativo mobile-first para estudantes universitários que trabalham, com microrrotinas flexíveis de 15 a 30 minutos; configuração inicial; Home com sugestão adaptada; treino guiado; Modo Sobrecarga; histórico, sequência e ajuste de metas.',body),P('<b>Requisitos enviados às duas ferramentas:</b> RF01 a RF14 e RNF01 a RNF08, incluindo persistência da configuração, registro parcial sem punição, início do treino em até três interações, acessibilidade, responsividade, privacidade local e consistência visual.',body),P('<b>Restrições comuns:</b> dados simulados, sem login, backend ou banco externo; botões amplos; resposta imediata; versão inicial preservada para comparação.',body),P('<b>Iterações adicionais:</b> não houve prompt de ajuste funcional aplicado à primeira versão do Protótipo 2. O único ajuste posterior foi no roteiro externo de QA, para tornar um seletor de botão exato; o código original permaneceu inalterado.',body),P('4. Protótipo 1',h1),P('<b>Ferramenta:</b> Claude (Claude Sonnet 5.5).<br/><b>Link de acesso público:</b> <link href="https://ihc-ds38.onrender.com/prototipo1/" color="blue">https://ihc-ds38.onrender.com/prototipo1/</link><br/><b>Verificação:</b> o endereço retornou HTTP 404 em 18/11/2026; requer correção da publicação antes da entrega.',body),P('Dados simulados, interface em português, mobile-first, modo claro e escuro.',body)]

labels=[('01-configuracao-inicial.png','Configuração inicial'),('02-home.png','Home com sugestão do dia'),('03-execucao.png','Execução do treino'),('04-modo-sobrecarga.png','Modo Sobrecarga'),('05-progresso.png','Progresso')]
def screenshot_grid(folder):
    items=[]
    for filename,label in labels:
        path=ROOT/'screenshots'/folder/filename if folder else ROOT/'screenshots'/filename
        items.append((fitted_image(path),P(label,caption)))
    return [
        Table([[items[0][0],items[1][0],items[2][0]],[items[0][1],items[1][1],items[2][1]]],colWidths=[5.7*cm]*3,hAlign='CENTER',style=[('VALIGN',(0,0),(-1,-1),'TOP')]),
        Spacer(1,.3*cm),
        Table([[items[3][0],items[4][0]],[items[3][1],items[4][1]]],colWidths=[5.7*cm]*2,hAlign='CENTER',style=[('VALIGN',(0,0),(-1,-1),'TOP')])]
story.append(PageBreak()); story.append(P('4. Protótipo 1 — capturas de tela',h1)); story.extend(screenshot_grid('prototipo1'))
story += [PageBreak(),P('5. Protótipo 2',h1),P('<b>Ferramenta:</b> OpenAI Codex (modelo GPT-5, ambiente Codex; plano da conta não exibido).<br/><b>Link de acesso público:</b> <link href="https://ihc-ds38.onrender.com/prototipo2/" color="blue">https://ihc-ds38.onrender.com/prototipo2/</link><br/><b>Verificação:</b> o endereço retornou HTTP 404 em 18/11/2026; requer correção da publicação antes da entrega.<br/><b>Resultado local testado:</b> <font name="Courier">/prototipo2/</font>.',body),P('Capturas realizadas após o teste do fluxo completo em viewport móvel de 390 px.',body)]
story.extend(screenshot_grid(None))
story += [PageBreak(),P('6. Análise comparativa',h1),P('Classificação baseada em execução dos fluxos no navegador. A = atendido; P = parcialmente atendido; N = não atendido.',body)]
vals={'RF01':'A','RF02':'A','RF03':'A','RF04':'A','RF05':'A','RF06':'A','RF07':'A','RF08':'A','RF09':'A','RF10':'A','RF11':'A','RF12':'P','RF13':'A','RF14':'A','RNF01':'P','RNF02':'A','RNF03':'A','RNF04':'P','RNF05':'A','RNF06':'A','RNF07':'A','RNF08':'A'}
p1={'RF12':'P','RNF01':'P','RNF04':'P'}
evidence={
'RF01':'P1: etapa inicial; P2: curso, Estágio/CLT/Outro e carga diária.','RF02':'P1: configuração/Home; P2: janela de 15 a 60 min persistida.','RF03':'Ambos permitem Casa/Academia/Parque e 15/20/30 min.','RF04':'Ambos oferecem objetivos pessoais editáveis/configuráveis.','RF05':'Ambos sugerem treino com tempo e local escolhidos.','RF06':'Botões de aceitar, trocar e ajustar foram acionados nos dois.','RF07':'P1 e P2 guiam exercício a exercício; iniciar, pausar e pular funcionam.','RF08':'Encerramento no meio registra Parcial e mostra acolhimento nos dois.','RF09':'Ambos exibem feedback e contagem semanal após conclusão.','RF10':'P1: 3/7/14 dias e 5/8/10 min; P2: mesmos períodos/durações.','RF11':'Histórico e sequência visíveis em ambos.','RF12':'Ambos reforçam positivamente dentro do app; não enviam notificação externa.','RF13':'Meta semanal ajustável e persistida nos dois.','RF14':'P1 retoma etapa; P2 salva cada escolha no localStorage e oferece Retomar.','RNF01':'Etapas curtas em ambos; não cronometrado com participantes reais.','RNF02':'P1 e P2: um toque em “Aceitar e começar” a partir da Home.','RNF03':'Mensagens de pausa e falha evitam culpa nos dois.','RNF04':'Alvos amplos e texto legível; contraste não medido formalmente.','RNF05':'Ambos testados em viewport móvel de 390 px.','RNF06':'Ações locais responderam sem espera de rede.','RNF07':'Dados apenas no navegador; sem conta, servidor ou banco externo.','RNF08':'Cores, cartões, botões e navegação uniformes em cada protótipo.'}
summary={r[0]:r[1] for r in reqs}
rows=[('ID','Resumo','Protótipo 1','Protótipo 2','Evidência / observação')]
for rid,_,_,_ in reqs: rows.append((rid,summary[rid],p1.get(rid,'A'),vals[rid],evidence[rid]))
story.append(table(rows,[1.05*cm,3.7*cm,1.65*cm,1.65*cm,9.0*cm]))
story += [PageBreak(),P('6. Análise comparativa — discussão',h1)]
answers=[
('1. Compatibilidade com requisitos funcionais e não funcionais','Sim, com ressalvas mensuráveis. Os dois protótipos executaram os fluxos funcionais centrais. Em ambos, lembretes existem apenas dentro do aplicativo (RF12 parcial), o tempo de configuração não foi validado com usuários (RNF01 parcial) e o contraste não passou por medição formal (RNF04 parcial).'),
('2. Tarefas e interações da HTA e MoLIC','Foram contempladas: configurar contexto e preferências; receber, trocar e ajustar uma sugestão; executar ou interromper uma rotina; ativar um plano mínimo; consultar histórico e ajustar meta. A interrupção retorna uma mensagem acolhedora e registra o resultado parcial, cobrindo o cenário de falha previsto na MoLIC.'),
('3. Requisitos atendidos, parciais ou não atendidos','Protótipo 1: 19 A, 3 P e 0 N. Protótipo 2: 19 A, 3 P e 0 N. Em ambos, RF12, RNF01 e RNF04 são parciais pelos motivos registrados na tabela. Nenhum requisito foi classificado como não atendido no escopo do protótipo estático.'),
('4. Principais diferenças','O Protótipo 1 usa React/Vite, oferece modo claro/escuro, perfil e calendário semanal, com maior densidade funcional. O Protótipo 2 usa HTML/CSS/JS sem build, apresenta hierarquia mais editorial, cartões amplos e navegação inferior enxuta. No P2, o Modo Sobrecarga comunica explicitamente “sem compensações”; a conclusão parcial enfatiza que escutar o corpo também é consistência. Os dois são interativos, mas o P1 expõe mais controles e o P2 reduz escolhas simultâneas.'),
('5. Dificuldades das ferramentas','No material recebido, o Claude entregou uma aplicação com dependências e compilação, o que aumenta o custo de publicação, embora exista uma versão standalone. O Codex interpretou todos os fluxos em uma geração. A limitação externa está na hospedagem: o domínio do Render foi informado, mas a raiz e os dois caminhos retornaram HTTP 404 no teste público de 18/11/2026. Nenhuma ferramenta produziu lembretes fora do app, coerente com a restrição de não usar backend.'),
('6. Melhor aderência às necessidades dos usuários','O Protótipo 2 apresenta ligeira vantagem para a persona cansada e com pouco tempo: a Home concentra contexto, sugestão e ação principal; a linguagem reconhece limites; e o plano mínimo explica o que muda sem criar dívida ou compensação. O Protótipo 1 permanece forte e mais completo, mas sua maior quantidade de opções pode elevar a carga cognitiva em momentos de exaustão.')]
for q,a in answers: story += [P(q,h2),P(a,body)]
story += [P('7. Protótipo selecionado',h1),P('<b>Protótipo escolhido:</b> Protótipo 2 — OpenAI Codex (EntrePausas).',body)]
criteria=[('Critério','Justificativa'),('Atendimento aos requisitos do software','Empata com o P1 na classificação (19 A, 3 P, 0 N) e demonstrou por teste os fluxos de persistência, sugestão, ajuste, treino, registro parcial, Sobrecarga, histórico e meta.'),('Compatibilidade com a modelagem de tarefas','Materializa a sequência HTA/MoLIC de configurar → receber sugestão → executar/pausar → registrar → acompanhar, incluindo tratamento acolhedor da interrupção.'),('Adequação às necessidades dos usuários','Prioriza baixa carga cognitiva, adaptação ao tempo disponível e linguagem sem culpa para um estudante cansado entre trabalho e aula.'),('Qualidade da organização e apresentação','Hierarquia clara, ação principal destacada, cartões consistentes e informação progressiva reduzem a competição visual.'),('Facilidade de navegação e interação','Um toque inicia o treino a partir da Home; alvos são amplos; a navegação inferior mantém três destinos estáveis.'),('Potencial para a avaliação de IHC (Etapa 5)','Os estados são observáveis e testáveis: troca de sugestão, mudança de tempo, pausa, saída parcial, ativação de sobrecarga, persistência e ajuste de meta permitem tarefas e métricas comparáveis.')]
story.append(table(criteria,[5.2*cm,11.8*cm]))
story += [Spacer(1,.3*cm),P('<b>Verificação da hospedagem:</b> os arquivos estão preparados na estrutura solicitada para um único Static Site do Render. Em 18/11/2026, a raiz e os caminhos <font name="Courier">/prototipo1/</font> e <font name="Courier">/prototipo2/</font> retornaram HTTP 404. É necessário corrigir a configuração/publicação e repetir o teste em janela anônima.',small)]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=1.5*cm,leftMargin=1.5*cm,topMargin=1.45*cm,bottomMargin=1.3*cm,title='TP1 P4 Prototipagem',author='Brayan Mendes de Carvalho; Joao Vitor Soares; Michael William Tang; Vitor de Freitas Rios')
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
