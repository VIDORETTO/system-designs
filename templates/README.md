<div align="center">
  <img src="../skill/assets/icon.svg" width="72" alt="Ícone dos templates de design system" />
  <h1>Design System Templates</h1>
  <p>
    <strong>Pacotes prontos para explorar, validar e reutilizar.</strong><br />
    Cada template reúne uma página viva, um manifesto machine-readable<br />
    e evidências suficientes para entender de onde as decisões vieram.
  </p>

  <p>
    <img src="https://img.shields.io/badge/ready%20to%20explore-FFD400?style=for-the-badge&labelColor=151515" alt="Pronto para explorar" />
    <img src="https://img.shields.io/badge/manifest%20%2B%20report-F75858?style=for-the-badge&labelColor=151515" alt="Manifesto e relatório" />
    <img src="https://img.shields.io/badge/evidence%20indexed-FFA43D?style=for-the-badge&labelColor=151515" alt="Evidências indexadas" />
  </p>

  <p>
    <a href="#o-que-existe-aqui">Visão rápida</a>
    ·
    <a href="#como-usar">Como usar</a>
    ·
    <a href="#template-incluido">Template incluído</a>
    ·
    <a href="#quality-gates">Qualidade</a>
  </p>
</div>

---

> Templates não são screenshots arquivados. São espécimes vivos de um design system, com contexto, regras e rastreabilidade.

<a id="o-que-existe-aqui"></a>

## ✦ O que existe aqui

A pasta <code>templates/</code> funciona como uma galeria de pacotes gerados pela skill [Extract Web Design System](../skill/README.md).

Cada pacote combina três camadas:

| Camada | Pergunta que responde | Artefato |
| --- | --- | --- |
| **Specimen** | “Como esse sistema se comporta visualmente?” | <code>report.html</code> |
| **Contract** | “Quais tokens e regras posso reutilizar?” | <code>design-system.json</code> |
| **Provenance** | “Qual é a origem e o limite de cada conclusão?” | <code>evidence/README.md</code> |

O objetivo é permitir leitura rápida, validação técnica e reaproveitamento responsável — sem transformar a referência em uma cópia literal do produto original.

## ◇ Categorias

As categorias são baseadas no domínio principal do produto. Formatos de interface, como hero, landing page ou dashboard, não criam categorias próprias e podem aparecer dentro de qualquer domínio.

| Categoria | Escopo |
| --- | --- |
| [SaaS](saas/README.md) | Software como serviço, IA, ferramentas para desenvolvedores e plataformas B2B |
| [Ecommerce](ecommerce/README.md) | Lojas, catálogos, varejo digital, checkout e compra online |
| [Finance](finance/README.md) | Bancos, fintechs, pagamentos, investimentos e contabilidade |
| [Healthcare](healthcare/README.md) | Clínicas, saúde, telemedicina, bem-estar e cuidado |
| [Education](education/README.md) | Escolas, cursos, treinamento e aprendizagem online |
| [Media](media/README.md) | Notícias, publicação, streaming, vídeo, áudio e conteúdo |
| [Portfolio](portfolio/README.md) | Portfólios pessoais, estúdios, agências e apresentação de trabalho |

### O que um template não é

- não é um pacote npm ou uma aplicação pronta para produção;
- não substitui a documentação específica de um produto real;
- não afirma comportamento quando a evidência só sustenta uma hipótese;
- não concede direitos sobre logos, textos, fontes, imagens ou marcas da referência;
- não deve carregar ativos protegidos quando espécimes neutros forem suficientes.

## ⌁ O ciclo de um template

~~~mermaid
flowchart LR
  A["Fonte observada"] --> B["Manifesto"]
  B --> C["Relatório vivo"]
  C --> D["Evidências"]
  D --> E["Reuso responsável"]
~~~

O pacote é lido em conjunto:

1. o relatório mostra o sistema em ação;
2. o manifesto transforma a leitura em contrato;
3. as evidências explicam a origem;
4. as limitações impedem que uma inferência vire regra absoluta;
5. o usuário decide o que adaptar para seu próprio produto.

<a id="como-usar"></a>

## ◎ Como usar

### 1 · Explorar visualmente

Abra o <code>report.html</code> do template no GitHub ou no navegador. Ele é a referência principal para:

- foundations e tokens;
- componentes e estados;
- responsive behavior;
- motion lab;
- composições;
- acessibilidade;
- evidências e export de tokens.

### 2 · Ler o contrato

Abra o <code>design-system.json</code> quando quiser:

- localizar um token semântico;
- gerar CSS, Tailwind ou Style Dictionary;
- alimentar um pipeline de design-to-code;
- comparar versões;
- escrever testes visuais ou de regressão.

### 3 · Conferir a proveniência

Leia <code>evidence/README.md</code> para entender:

- quais rotas foram capturadas;
- em quais viewports;
- quais interações foram realmente testadas;
- quais dados foram observados no DOM/CSS;
- quais estados ficaram inacessíveis;
- quais ativos foram deliberadamente omitidos.

### 4 · Validar ou regenerar

A partir da raiz do repositório:

~~~bash
python3 skill/scripts/validate_design_system.py \
  templates/saas/alethe-design-system/design-system.json
~~~

Gere uma nova baseline do relatório:

~~~bash
python3 skill/scripts/render_design_system_report.py \
  templates/saas/alethe-design-system/design-system.json \
  /tmp/design-system-report.html
~~~

Para servir os arquivos locais e testar links, clipboard e interação:

~~~bash
python3 -m http.server 4173
~~~

Depois, abra:

~~~text
http://localhost:4173/templates/saas/alethe-design-system/report.html
~~~

<a id="template-incluido"></a>

## ◇ Template incluído

### <code>saas/alethe-design-system/</code>

Um pacote autocontido que reconstrói, em nível de sistema, a linguagem visual e interativa do Alethe Agents.

| Entrega | Status |
| --- | --- |
| Página viva do design system | pronta |
| Tokens e regras normalizados | prontos |
| Evidências e limitações | documentadas |
| Dependências de runtime do relatório | nenhuma |
| Validação do manifesto | 0 erros · 0 warnings |
| Captura principal | pública · desktop · 1363 × 936 · DPR 1 |
| Confiança geral | medium |

### O que o pacote demonstra

- frame técnico e composição centralizada;
- contraste operacional em superfícies escuras;
- tipografia display, sans e mono;
- temas tratados como acento;
- estados de agentes, dots, panes, grids e canvas;
- motion com laboratório de replay, pause e slow mode;
- espécimes neutros em CSS/SVG;
- navegação interna, foco visível, tabs, live regions e reduced motion;
- exportação de tokens para implementação.

### Direção visual

O template trabalha com cinco ideias principais:

| Princípio | Expressão |
| --- | --- |
| **Technical frame** | Frame central, trilhos, hairlines e marcas de registro |
| **Operational contrast** | Quase-preto, branco forte e um acento escasso |
| **Proof through UI** | Terminais, árvores, grids, dots e panes para mostrar capacidade |
| **Theme as accent** | A arquitetura permanece; o sinal cromático muda |
| **Dense details, quiet rhythm** | Microinformação operacional equilibrada por espaço negativo |

O relatório não replica a landing page original. Ele preserva regras e padrões usando conteúdo neutro quando a referência continha arte, marca ou material protegido.

### <code>ecommerce/garage311-design-system/</code>

Um pacote de ecommerce que reconstrói a linguagem de uma storefront de peças e acessórios, cobrindo catálogo, detalhe de produto, fitment, merchandising e substituições mobile.

| Entrega | Status |
| --- | --- |
| Página viva do design system | pronta |
| Tokens e regras normalizados | prontos |
| Evidências e limitações | indexadas, com capturas raster omitidas por política de publicação |
| Dependências de runtime do relatório | nenhuma |
| Validação do manifesto | 0 erros · 0 warnings |
| Cobertura principal | pública · home e produto · 1440 × 900 + 390 × 844 |
| Confiança geral | medium |

O pacote demonstra como a mesma gramática organiza descoberta e conversão: hero, benefícios, rails de produtos, preço/Pix, galeria, aplicação, confiança operacional, suporte e footer. O relatório usa espécimes neutros e mantém os links das rotas observadas.

## ⟡ Anatomia do pacote

~~~text
saas/
├── README.md
│   └── escopo da categoria e regra de classificação
└── alethe-design-system/
    ├── README.md
    │   └── guia de uso, direção visual e limitações
    ├── report.html
    │   └── página viva, autocontida e interativa
    ├── design-system.json
    │   └── tokens, regras, componentes e evidências
    └── evidence/
        └── README.md
            └── índice de capturas, probes e coverage note
~~~

### Papel de cada arquivo

| Arquivo | Serve para |
| --- | --- |
| <code>README.md</code> | Entender o pacote, seus princípios, uso recomendado e limitações |
| <code>report.html</code> | Explorar o sistema através de espécimes visuais e interativos |
| <code>design-system.json</code> | Consumir tokens e regras em automação |
| <code>evidence/README.md</code> | Rastrear fontes, interações, captura e cobertura |

## ◌ O que conferir antes de reutilizar

Use o template como referência, não como verdade universal. Antes de levar uma regra para um produto:

- confirme se ela aparece em mais de uma rota ou componente;
- diferencie valor observado de token semântico;
- veja se a regra muda por estado, tema ou breakpoint;
- teste a composição em pelo menos dois viewports;
- valide contraste, foco, teclado e reduced motion;
- substitua espécimes por identidade e conteúdo próprios;
- confirme licenças de fontes, imagens, ícones e marcas.

## ✓ Quality gates

Um novo template só deve entrar nesta pasta quando:

- existir uma página viva que use os próprios tokens;
- houver um manifesto válido em <code>design-system.json</code>;
- os claims importantes tiverem evidência e confiança;
- componentes exibirem anatomia, variantes e estados;
- responsive behavior estiver renderizado ou explicitamente limitado;
- motion tiver trigger, duração, easing e reduced motion quando observável;
- o relatório for navegável por teclado e tiver foco visível;
- links internos, IDs, JavaScript e CSS forem validados;
- o pacote não copiar conteúdo protegido desnecessariamente;
- README e evidence index explicarem gaps e como reproduzir.

<a id="adicionar-template"></a>

## ⊞ Como adicionar um novo template

1. Extraia o sistema com a skill em <code>../skill/SKILL.md</code>.
2. Escolha uma categoria de domínio existente; crie uma nova somente quando o produto não couber em nenhuma categoria atual.
3. Crie uma pasta com nome estável e descritivo em <code>templates/&lt;categoria&gt;/</code>.
4. Gere <code>design-system.json</code> e valide o manifesto.
5. Gere <code>report.html</code> e faça a página usar os tokens extraídos.
6. Adicione <code>evidence/README.md</code> com IDs, fontes, contexto e limitações.
7. Escreva o README do pacote com objetivo, direção visual, estrutura, uso e direitos.
8. Atualize este índice com o novo pacote.
9. Teste a experiência em viewport largo, viewport estreito, teclado e reduced motion.

### Convenção recomendada

~~~text
templates/
└── categoria/
    └── nome-do-template/
        ├── README.md
        ├── design-system.json
        ├── report.html
        └── evidence/
            └── README.md
~~~

Não adicione assets de referência por padrão. Se uma imagem ou fonte for necessária, documente a origem, a licença e por que um espécime neutro não atende ao caso.

## ⌂ Privacidade, direitos e limites

- Preserve apenas evidências que possam ser mantidas no pacote com autorização.
- Não ultrapasse controles de acesso para aumentar a cobertura.
- Não inclua dados pessoais, segredos ou estados privados.
- Prefira CSS/SVG neutro a logos, screenshots e imagens proprietárias.
- Deixe claro quando o mobile foi inferido a partir de CSS e ainda não foi renderizado.
- Descreva diferenças materiais entre fonte e espécime; não prometa pixel perfection sem comparação equivalente.

## ≡ Leituras recomendadas

| Arquivo | Quando abrir |
| --- | --- |
| [README da raiz](../README.md) | Para entender o repositório inteiro |
| [README da skill](../skill/README.md) | Para executar uma nova extração |
| [Alethe README](saas/alethe-design-system/README.md) | Para estudar um pacote completo |
| [Alethe evidence index](saas/alethe-design-system/evidence/README.md) | Para ver o modelo de proveniência |
| [Extraction schema](../skill/references/extraction-schema.md) | Para escrever o manifesto |
| [Report spec](../skill/references/report-spec.md) | Para construir o relatório vivo |
| [Acquisition playbook](../skill/references/acquisition-playbook.md) | Para planejar captura e coverage |

---

<div align="center">
  <sub>Explore the specimen · inspect the contract · respect the evidence</sub>
</div>



## ✧ Fixture de Experience Layer

Além dos domínios, a galeria agora inclui templates/media/experience-layer/. Ele é um
fixture neutro para sites cuja linguagem depende de hero cinematográfico, vídeo
de background, poster, textura, efeitos, cursor/scroll response e motion.

O pacote demonstra:

- design-system.json com meta.schema_version: 2;
- report.html com mídia local neutra, controls de motion e reduced-motion;
- evidence/ com SVGs de poster/still e mapa de proveniência;
- política de vídeo que separa autoplay observado, fallback recomendado e limites
  de performance.

