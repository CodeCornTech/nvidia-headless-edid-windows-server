# NVIDIA Headless EDID Fix — Guida italiana

**Correzione delle finestre bianche, dello scroll e del ridimensionamento errato su Windows Server senza monitor, tramite emulazione EDID NVIDIA.**

[English README](README.md) · [Problemi noti](docs/troubleshooting.md) · [Rollback](docs/rollback.md) · [Stato delle verifiche](docs/validation-matrix.md)

> **Caso reale, non garanzia universale.** La procedura è stata risolta su Windows Server 2022 Datacenter con NVIDIA Quadro P620. Servono sia l'EDID forzato sia una corretta configurazione del monitor principale in Windows. Caricare soltanto il file EDID **non** aveva eliminato tutti i problemi. Persistenza al riavvio, hot-plug e altre GPU non sono ancora state verificate.

## Sintomi osservati

- Scroll e menu a tendina di **Impostazioni Windows** difettosi, coordinate del mouse incoerenti.
- Finestre completamente bianche in **Server Manager**, **Supremo** e altre applicazioni.
- Start e applicazioni rimpicciolite o non estese correttamente sullo schermo.
- **AnyDesk: In attesa dati immagine**; rendering irregolare in RustDesk.
- Driver NVIDIA indicato come funzionante, nonostante l'assenza di monitor.

## Configurazione del caso

| Voce | Valore |
| --- | --- |
| Sistema | Windows Server 2022 Datacenter |
| Scheda | NVIDIA Quadro P620 |
| Driver NVIDIA | 582.99 / 32.0.15.8299 |
| RTX Desktop Manager | 205.40 |
| Schermi fisici | Nessuno |
| Porta dedicata | Mini DisplayPort 4 |
| Origine EDID | **File**, da topologia NVIDIA |
| Modalità | 1920×1080, 60 Hz, RGB 8 bit, SDR |
| Applicazioni verificate nel troubleshooting | RustDesk, Supremo, AnyDesk |
| Data caso | 26 novembre 2026 |

Per evitare di pubblicare identificativi interni, negli esempi il monitor si chiama **HEADLESS-1080**.

## Prima di intervenire

**Non perdere l'unico accesso remoto disponibile.** Mantieni un percorso di recupero (sessione di riserva o console fisica/out-of-band), annota la porta e la disposizione precedente degli schermi e lascia attivo un eventuale display virtuale temporaneo fino alla fine del test. Nessuna disinstallazione di driver, reset distruttivo o modifica RDS è richiesta dalla procedura.

## Procedura

### 1. Disponi temporaneamente di uno schermo funzionante

Se l'interfaccia non viene disegnata, un monitor virtuale temporaneo di un programma di assistenza remota può permettere di usare le Impostazioni e il pannello NVIDIA. Serve **solo per configurare e recuperare la sessione**, non è una dipendenza della soluzione finale documentata.

### 2. Prepara un EDID valido

Da **Pannello di controllo NVIDIA → Workstation → Visualizza la topologia del sistema → EDID**, esporta l'EDID di un monitor compatibile oppure usa un EDID di provenienza verificata, adeguato alla modalità desiderata.

Nel caso reale, NVIDIA ha accettato un EDID locale 1080p60. Il repository **non distribuisce un blob EDID generico non verificato**. La correttezza del checksum non basta a garantire che qualsiasi file sia adatto a ogni GPU.

### 3. Carica l'EDID sulla porta libera

Seleziona **Gestisci EDID → Carica**:

1. Scegli il file EDID.
2. Seleziona **una sola porta inutilizzata** della Quadro.
3. Nel nostro caso scegli **DisplayPort (4)**, segnale **DisplayPort (digitale)**.
4. Conferma l'avvertenza e clicca **Carica EDID**.
5. In **Visualizza la topologia del sistema** verifica **Collegato** e **EDID (File)**.
6. In **Impostazioni schermo avanzate** controlla la modalità prevista, nel caso: **1920×1080 a 60 Hz**.

**Non fermarti a questo risultato.** Sul server testato NVIDIA riconosceva già il monitor, ma Windows presentava ancora scroll e dimensioni errati.

### 4. Configura correttamente il desktop Windows

**Lascia attivo il monitor virtuale temporaneo** durante questi passaggi:

1. Apri **Impostazioni → Sistema → Schermo** (non soltanto Schermo avanzato).
2. Premi **Identifica** e seleziona il monitor NVIDIA caricato da EDID, ad esempio **HEADLESS-1080**.
3. Imposta **1920×1080 a 60 Hz**.
4. Imposta **Ridimensionamento 100%** come riferimento diagnostico iniziale; se necessario allinea anche quello del monitor temporaneo.
5. Se entrambi sono visibili, usa **Estendi questi schermi**.
6. Sul monitor NVIDIA seleziona **Imposta come schermo principale** se non lo è già.
7. Applica, riapri **Impostazioni, Server Manager, Start, Supremo e AnyDesk** e verifica scroll, menu, coordinate, dimensioni e video remoto.

La risoluzione finale è stata confermata dall'utilizzatore dopo la correzione della configurazione schermo/principale. Non è dimostrato che tutte le singole impostazioni siano indispensabili in ogni ambiente.

### 5. Rimuovi il display temporaneo soltanto a test conclusi

Dopo che lo schermo NVIDIA funziona come desktop, disattiva il monitor virtuale temporaneo **mantenendo un accesso di riserva**, quindi ripeti tutti i controlli.

La risoluzione delle anomalie UI e remote è stata confermata nel caso descritto; **la persistenza dopo riavvio non è stata ancora verificata**.

## Diagnostica senza modifiche

~~~powershell
Get-CimInstance Win32_VideoController |
  Select-Object Name,DriverVersion,Status,CurrentHorizontalResolution,CurrentVerticalResolution

Get-PnpDevice -Class Display,Monitor |
  Format-Table Class,Status,FriendlyName,InstanceId -AutoSize

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::AllScreens |
  Select-Object DeviceName,Primary,
    @{Name='Risoluzione';Expression={"$($_.Bounds.Width)x$($_.Bounds.Height)"}} |
  Format-Table -AutoSize

nvidia-smi
~~~

Non interpretare automaticamente **Disp.A Off** o **Microsoft Remote Display Adapter: Unknown** come guasti. Non confondere il numero dello schermo nelle Impostazioni con il nome API come DISPLAY1 o DISPLAY5.

## Se colleghi un monitor fisico

Riserva la porta 4 all'emulazione EDID e usa un'altra uscita per lo schermo reale, se possibile. L'EDID forzato può ignorare gli eventi di collegamento/scollegamento su quella porta. La duplicazione e il cambio automatico del primario **non sono garantiti** e vanno testati.

## Riferimenti e recupero

- [Problemi e diagnosi](docs/troubleshooting.md)
- [Rollback sicuro](docs/rollback.md)
- [Matrice di verifica](docs/validation-matrix.md)
- [Contributi della community](CONTRIBUTING.md)
- [NVIDIA — Gestione EDID su Quadro/NVS](https://nvidia.custhelp.com/app/answers/detail/a_id/3301)
- [NVIDIA — Managing a Display EDID on Windows](https://nvidia.custhelp.com/app/answers/detail/a_id/3569)
- [Microsoft — Enumeration and Display Control](https://learn.microsoft.com/en-us/windows/win32/gdi/enumeration-and-display-control)

**Nota:** documentazione indipendente di CodeCorn Technology, senza affiliazione o approvazione da NVIDIA o Microsoft. Licenza [MIT](LICENSE).
