const { PDFDocument } = require("pdf-lib");

const LOGO_BASE64 = "/9j/4AAQSkZJRgABAQEASABIAAD/4Q6aRXhpZgAATU0AKgAAAAgABgESAAMAAAABAAEAAAEaAAUAAAABAAAAVgEbAAUAAAABAAAAXgEoAAMAAAABAAIAAAITAAMAAAABAAEAAIdpAAQAAAABAAAAZgAAAMAAAABIAAAAAQAAAEgAAAABAAeQAAAHAAAABDAyMjGRAQAHAAAABAECAwCgAAAHAAAABDAxMDCgAQADAAAAAQABAACgAgAEAAAAAQAAAfSgAwAEAAAAAQAAAfSkBgADAAAAAQAAAAAAAAAAAAYBAwADAAAAAQAGAAABGgAFAAAAAQAAAQ4BGwAFAAAAAQAAARYBKAADAAAAAQACAAACAQAEAAAAAQAAAR4CAgAEAAAAAQAADWwAAAAAAAAASAAAAAEAAABIAAAAAf/Y/+AAEEpGSUYAAQEAAAEAAQAA/9sAQwAGBAUGBQQGBgUGBwcGCAoQCgoJCQoUDg8MEBcUGBgXFBYWGh0lHxobIxwWFiAsICMmJykqKRkfLTAtKDAlKCko/9sAQwEHBwcKCAoTCgoTKBoWGigoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo/8AAEQgAoACgAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A90ooor8mPoAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigApkk0UWPMkRM9NzAZrlfiZr8+geHDLZttup5BDG/8AcyCS35D9a4LwZ4FPinTH1bVtQuA0zsEx8zNjgsSffP5V9Jl+Q0quCeY42t7KlflXuuTb9Lr+kzz6+NlGt7ClDmla+9rHtIIIyDkGlrwvSr6/8C+Nv7Le6eaxEqpIhPysjYwwHYgHP4YpnxkY/wDCZnk8W8ePbrXqUeC5VcbDDxrL2dSHPGajutOl1bddTnlmyjRdRw96Ls1f9T3SSWOPHmOq56bjjNPryLWfh1fS6NdapqerPcaokTTMpG5eBkrnP/1qs/BTWrq5+2aXcyvLFCglh3HJQZwR9ORXFX4cofUKmNweIVT2bSkuVrfs3v8AdqbQx8/bRpVafLzba3+8k8PeOdW1Dx4NJnFt9kaeWP5UIYBQxHOfYV6hmvBvBv8AyVhP+vq4/wDQXp2rs3hT4pNcAlYDcCYnPWOT738yPwr6HN+GKGLxioYS1OSoqaSXxO7XdWe2upwYXMZ0qTnV95c9r322Pd6K5H4pan/Z3g278t9styRAhB/vdf8Ax0GsX4IaeYNDvb5hg3MwRf8AdQdfzJ/Kvj6eS82VTzOc7WlyqNviel9b6W16PY9WWLtiVh0r6Xb7HpFFFFeGdgUUUUAFFFFABRRRQAUUUUAcP8XtJn1PwuJLVGkktJRMyqMkrgg4+mQfwrnfht430nSvDq6fqsrwSQOxRvLLB1Jz2B5yTXrVYl74T0G9mMtxpVq0jHJYJtJPvjrX1OAzrCPLv7MzCEnBS5k4tJp/PTv955tbCVfb/WKDSdrN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oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDzK9+LVlDdSx2+mzzRIxVZDIF3Y74waiX4vWxYB9JmC9yJgT/KvIX+831pK/eY8DZMopOk3580v8z4t5xi7/F+CPqmwuor6xt7uAkwzxrKhI5IYZH86sVjeDP+RS0b/rzi/wDQRWzX4di6So15047Jtfcz7GlJygpPqgooornLCiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK4T4leMz4fgFlp5VtSmXduIyIV/vY9Tzge2T792XZdXzLERw2HV5P7kurfkjGvXhh4OpN6I6fW9f0vRIw2p3kUBPKoTlz9FGTXF33xZ0uJiLOxu7jB+85WMH+Z/SvG7q4mu7h57qWSa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";
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

module.exports = async function (req, res) {
  if (req.method !== "POST") {
    return res.status(405).send("Method not allowed");
  }

  const body = req.body;
  const { pdfs, action } = body;

  // --- AKCIA: Pridanie loga do PDF ---
  if (action === "addLogo") {
    try {
      const results = [];
      const logoBytes = Buffer.from(LOGO_BASE64, "base64");

      for (const pdfB64 of pdfs) {
        const pdfBytes = Buffer.from(pdfB64, "base64");
        const pdfDoc = await PDFDocument.load(pdfBytes, { ignoreEncryption: true });
        const logoImage = await pdfDoc.embedJpg(logoBytes);

        const pages = pdfDoc.getPages();
        const pagesToStamp = Math.min(3, pages.length);

        for (let i = 0; i < pagesToStamp; i++) {
          const page = pages[i];
          const { width, height } = page.getSize();
          const logoW = 80;
          const logoH = (logoImage.height / logoImage.width) * logoW;
          page.drawImage(logoImage, {
            x: width - logoW - 20,
            y: height - logoH - 15,
            width: logoW,
            height: logoH,
            opacity: 0.85,
          });
        }

        const modifiedBytes = await pdfDoc.save();
        results.push(Buffer.from(modifiedBytes).toString("base64"));
      }

      return res.status(200).json({ pdfsWithLogo: results });
    } catch (err) {
      return res.status(500).json({ error: "Chyba pri vkladaní loga: " + err.message });
    }
  }

  // --- AKCIA: Analýza PDF cez Claude Vision ---
  if (action === "analyze") {
    try {
      const content = [];

      content.push({
        type: "text",
        text: `Analyzuj tieto cenové ponuky od firmy Climax. Pre každé PDF vráť JSON objekt s týmito poľami:
- nazov_produktu: názov produktu (napr. "Z-90 Noval", "EXT 16")
- pocet_ks: celkový počet kusov (číslo)
- cena_bez_dph: celková cena bez DPH v EUR (číslo)
- cena_s_dph: celková cena s DPH v EUR (číslo)
- zlava_percent: zľava v % ak je uvedená (číslo alebo null)

Použi hodnoty z riadku "Cena spolu bez DPH" a "Cena spolu s DPH".
Vrát POLE JSON objektov - jeden objekt za každé PDF v poradí ako sú priložené.
Vráť IBA validné JSON pole, nič iné, žiadny markdown, žiadne \`\`\`.`
      });

      for (let i = 0; i < pdfs.length; i++) {
        content.push({
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: pdfs[i],
          },
        });
      }

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
          "anthropic-beta": "pdfs-2024-09-25",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 1024,
          messages: [{ role: "user", content }],
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        return res.status(500).json({ error: "Claude API chyba: " + JSON.stringify(data) });
      }

      const rawText = data.content[0].text.trim();
      const analyzed = JSON.parse(rawText);

      const celkovaBezDph = analyzed.reduce((sum, p) => sum + (p.cena_bez_dph || 0), 0);
      const celkovaSdph = analyzed.reduce((sum, p) => sum + (p.cena_s_dph || 0), 0);

      return res.status(200).json({
        produkty: analyzed,
        celkova_bez_dph: Math.round(celkovaBezDph * 100) / 100,
        celkova_s_dph: Math.round(celkovaSdph * 100) / 100,
      });
    } catch (err) {
      return res.status(500).json({ error: "Chyba analýzy: " + err.message });
    }
  }

  // --- AKCIA: Generovanie emailu ---
  if (action === "generateEmail") {
    try {
      const { produkty, celkova_bez_dph, celkova_s_dph } = body;

      const produktyText = produkty
        .map((p, i) => `${i + 1}. ${p.nazov_produktu}: ${p.pocet_ks} ks, ${p.cena_bez_dph.toFixed(2)} EUR bez DPH / ${p.cena_s_dph.toFixed(2)} EUR s DPH`)
        .join("\n");

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": ANTHROPIC_API_KEY,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 600,
          messages: [{
            role: "user",
            content: `Napíš profesionálny sprievodný email v slovenčine k priloženým cenovým ponukám od firmy Only servis s.r.o.

Produkty v prílohe:
${produktyText}

Celková suma bez DPH: ${celkova_bez_dph.toFixed(2)} EUR
Celková suma s DPH: ${celkova_s_dph.toFixed(2)} EUR

Odosielateľ: Machala Roman, Only servis s.r.o., Lermontovova 911/3, 811 05 Bratislava, tel: 0903 533 534

Požiadavky na email:
- Oslovi zákazníka "Vážený zákazník" (bez mena)
- Stručne zhrň čo je v prílohách (každý produkt na nový riadok)
- Uveď celkovú sumu
- Zdvorilý záver s výzvou na kontakt
- BEZ markdown formátovania, BEZ tučného písma
- Maximálne 150 slov`,
          }],
        }),
      });

      const data = await response.json();
      const emailText = data.content[0].text.trim();
      return res.status(200).json({ emailText });
    } catch (err) {
      return res.status(500).json({ error: "Chyba generovania emailu: " + err.message });
    }
  }

  // --- AKCIA: Odoslanie emailu cez Gmail ---
  if (action === "sendEmail") {
    try {
      const { emailText, pdfsWithLogo, pdfNames, recipientEmail, accessToken } = body;

      const boundary = "onlyservis_boundary_" + Date.now();
      let mimeMessage = [
        `MIME-Version: 1.0`,
        `To: ${recipientEmail}`,
        `From: Machala Roman <info@climaxsk.sk>`,
        `Subject: Cenová ponuka Only servis s.r.o.`,
        `Content-Type: multipart/mixed; boundary="${boundary}"`,
        ``,
        `--${boundary}`,
        `Content-Type: text/plain; charset=UTF-8`,
        ``,
        emailText,
        ``,
      ].join("\r\n");

      for (let i = 0; i < pdfsWithLogo.length; i++) {
        const fileName = pdfNames[i] || `ponuka_${i + 1}.pdf`;
        mimeMessage += [
          `--${boundary}`,
          `Content-Type: application/pdf`,
          `Content-Transfer-Encoding: base64`,
          `Content-Disposition: attachment; filename="${fileName}"`,
          ``,
          pdfsWithLogo[i],
          ``,
        ].join("\r\n");
      }

      mimeMessage += `--${boundary}--`;

      const encoded = Buffer.from(mimeMessage)
        .toString("base64")
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=+$/, "");

      const gmailRes = await fetch(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ raw: encoded }),
        }
      );

      if (!gmailRes.ok) {
        const err = await gmailRes.json();
        return res.status(500).json({ error: "Gmail chyba: " + JSON.stringify(err) });
      }

      return res.status(200).json({ success: true });
    } catch (err) {
      return res.status(500).json({ error: "Chyba odosielania: " + err.message });
    }
  }

  return res.status(400).json({ error: "Neznáma akcia" });
};
