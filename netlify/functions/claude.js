const https = require('https');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const body = JSON.parse(event.body);
  const action = body.action;

  // Action: analyze — extract text from PDF and analyze with Claude
  if (action === 'analyze') {
    const pdfBase64 = body.pdfBase64;
    const pdfBytes = Buffer.from(pdfBase64, 'base64');
    
    // Extract text from PDF using regex on raw bytes
    const pdfStr = pdfBytes.toString('latin1');
    const texts = [];
    
    // Method 1: BT/ET text blocks
    const btEt = /BT([\s\S]*?)ET/g;
    let m;
    while ((m = btEt.exec(pdfStr)) !== null) {
      const block = m[1];
      // Tj and TJ operators
      const tjMatches = block.match(/\(([^)]{1,300})\)\s*Tj/g) || [];
      const tjArrMatches = block.match(/\[([^\]]{1,500})\]\s*TJ/g) || [];
      for (const t of tjMatches) {
        const txt = t.replace(/\(([^)]*)\)\s*Tj/, '$1').trim();
        if (txt.length > 0) texts.push(txt);
      }
      for (const t of tjArrMatches) {
        const parts = t.match(/\(([^)]*)\)/g) || [];
        texts.push(parts.map(p => p.slice(1,-1)).join(''));
      }
    }
    
    // Method 2: stream content
    const streamMatches = pdfStr.match(/stream([\s\S]*?)endstream/g) || [];
    for (const s of streamMatches) {
      const readable = s.replace(/[^\x20-\x7E\n]/g, ' ').replace(/\s+/g, ' ');
      if (readable.includes('EUR') || readable.includes('Cena') || readable.includes('Pocet')) {
        texts.push(readable.substring(0, 1000));
      }
    }
    
    const extractedText = texts.join(' ').replace(/\s+/g, ' ').substring(0, 5000);
    
    const claudeResponse = await callClaude({
      model: 'claude-sonnet-4-6',
      max_tokens: 400,
      system: 'Si expert na analyzu cenovych ponuk. Odpovedaj VYHRADNE platnym JSON objektom, bez textu pred ani za nim.',
      messages: [{
        role: 'user',
        content: 'Z tohto textu cenovej ponuky extrahuj: produkt (nazov ako EXT 16, Posuvne siete v listach, IDX domykac atd), ks (pocet kusov, cislo pri "Pocet"), cena_bez_dph (EUR pri "Cena spolu bez DPH"), cena_s_dph (EUR pri "Cena spolu s DPH"). Vrat JEDINE: {"produkt":"...","ks":N,"cena_bez_dph":X,"cena_s_dph":Y}\n\nTEXT:\n' + extractedText
      }]
    });
    
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(claudeResponse)
    };
  }

  // Action: generate-email
  if (action === 'generate-email') {
    const result = await callClaude(body.payload);
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(result)
    };
  }

  // Default: proxy to Claude API directly
  try {
    const result = await callClaude(body);
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify(result)
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};

function callClaude(payload) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(payload);
    const req = https.request({
      hostname: 'api.anthropic.com',
      path: '/v1/messages',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch(e) { reject(new Error('Parse error: ' + body.substring(0,200))); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}
