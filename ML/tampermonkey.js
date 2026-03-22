let ultima_vaga = null;

// MUTATION OBSERVER
const observer = new MutationObserver(() => { main(); });
observer.observe(document.body, { childList: true, subtree: true });
console.log("👀 Observando mudanças na página...");

function main() {

      // BUSCA DADOS DA VAGA
      const texto_vaga = extrair_vaga();
      if (!texto_vaga) { return; }

      // REMOVE CONTAINER ANTIGO
      const container_antigo = document.getElementById("container-botoes");
      if (container_antigo) { container_antigo.remove(); }

      // AVALIA VAGA COMPARANDO COM O MODELO E CRIA BOTOES PARA TREINAR O MODELO
      avaliar_vaga(texto_vaga);
      criar_botoes(texto_vaga);
}

function extrair_vaga() {

      // EXTRAI TITULO E VAGA PARA O MODELO
      const titulo_vaga = document.querySelector(".job-details-jobs-unified-top-card__job-title a")?.innerText.trim() || document.querySelector('a[href*="/jobs/view/"]')?.innerText.trim() || document.querySelector("#h1")?.innerText.trim();
      const descricao_vaga = document.querySelector("#job-details")?.innerText.trim() || document.querySelector('[data-testid="expandable-text-box"]')?.innerText.trim() || document.querySelector('[data-testid="section-Descrição da vaga-title"]')?.parentElement?.innerText.trim();
      if (!titulo_vaga || !descricao_vaga) { console.log("❌ Titulo ou descrição não encontrada."); return; }

      // BLOQUEIA VAGA JA PROCESSADA
      const texto_vaga = titulo_vaga + "\n\n" + descricao_vaga;
      if (texto_vaga === ultima_vaga) { return; }
      ultima_vaga = texto_vaga

      console.log("✅ Vaga extraída com sucesso.");
      return texto_vaga
}

function avaliar_vaga(texto_vaga) {

      // ENVIA VAGA PARA COMPARACAO COM MODELO
      GM_xmlhttpRequest({
            method: "POST", url: "http://localhost:8000/avaliacoes", headers: {"Content-Type": "application/json"}, data: JSON.stringify({"texto_vaga": texto_vaga}),
            onload: (response) => { const data = JSON.parse(response.responseText); console.log(data.msg); }
      });
}

function treinar_modelo(texto_vaga, label) {

      // ENVIAR VAGA PARA TREINAMENTO
      GM_xmlhttpRequest({
            method: "POST", url: "http://localhost:8000/treinamentos", headers: {"Content-Type": "application/json"}, data: JSON.stringify({"texto_vaga": texto_vaga, "label": label}),
            onload: (response) => { const data = JSON.parse(response.responseText); console.log(data.msg); }
      });
}

function criar_botoes(texto_vaga) {

      // EVITAR DUPLICACOES
      if (document.getElementById("container-botoes")) { return; }

      // CRIAR CONTAINER PARA OS BOTOES
      const container = document.createElement("div");
      container.id = "container-botoes";
      container.style.marginTop = "20px";

      // BOTAO GOSTEI
      const botao_gostei = document.createElement("button");
      botao_gostei.innerText = "👍 Vaga compatível."
      botao_gostei.style.marginRight = "10px";
      botao_gostei.style.fontSize = "15px";
      botao_gostei.style.backgroundColor = "white";

      // BOTAO NAO GOSTEI
      const botao_nao_gostei = document.createElement("button");
      botao_nao_gostei.innerText = "👎 Vaga não compatível.";
      botao_nao_gostei.style.fontSize = "15px";
      botao_nao_gostei.style.backgroundColor = "white";

      // EVENTO AO CLICAR
      botao_gostei.onclick = () => treinar_modelo(texto_vaga, 0);
      botao_nao_gostei.onclick = () => treinar_modelo(texto_vaga, 1);

      container.appendChild(botao_gostei);
      container.appendChild(botao_nao_gostei);

      const inserir_em = document.querySelector("#job-details") || document.querySelector('[data-testid="expandable-text-box"]') || document.querySelector('[data-testid="section-Descrição da vaga-title"]');
      if (!inserir_em) { console.log(); return; }

      inserir_em.parentNode.insertBefore(container, inserir_em);
      console.log("✅ Botões inseridos com sucesso.");
}
