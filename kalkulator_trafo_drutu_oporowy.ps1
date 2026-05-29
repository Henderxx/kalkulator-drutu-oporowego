# KALKULATOR PRZECINARKI STYROPINU - WERSJA POWERSHELL

function Clear-Screen {
    Clear-Host
}

function Write-Header($title) {
    Write-Host ("=" * 70) -ForegroundColor White
    Write-Host $title.PadLeft(35 + [Math]::Floor($title.Length/2)).PadRight(70) -ForegroundColor White
    Write-Host ("=" * 70) -ForegroundColor White
}

function Write-Section($title) {
    Write-Host ""
    Write-Host $title -ForegroundColor Cyan
    Write-Host ("-" * 50) -ForegroundColor Gray
}

function Write-Result($label, $value, $unit="", $color="Green") {
    $formattedLabel = $label.PadRight(35)
    Write-Host "$formattedLabel : " -NoNewline
    Write-Host "$value $unit" -ForegroundColor $color
}

function Write-WarningMsg($text) {
    Write-Host "Ostrzezenie: $text" -ForegroundColor Yellow
}

function Write-Info($text) {
    Write-Host "Info: $text" -ForegroundColor Blue
}

function Write-Danger($text) {
    Write-Host "Uwaga: $text" -ForegroundColor Red
}

function Get-WireSize($current) {
    # Gestosc pradu dla miedzi: 3A/mm2 (bezpieczna wartosc)
    $currentDensity = 3.0  # A/mm2
    
    # Wymagany przekroj z zapasem 2x
    $minArea = ($current * 2) / $currentDensity
    
    # Srednica przewodu (mm) - zakladamy przekroj kola
    $diameter = 2 * [Math]::Sqrt($minArea / [Math]::PI)
    
    return $minArea, $diameter
}

function Show-WireTable {
    Write-Host "Prad maks. / Przekroj min. / Srednica / Typ przewodu"
    Write-Host "----------------------------------------------------"
    Write-Host "1A         / 0.7 mm2       / 1.0 mm   / cienki (np. krokodylek)"
    Write-Host "2A         / 1.3 mm2       / 1.3 mm   / cienki"
    Write-Host "3A         / 2.0 mm2       / 1.6 mm   / sredni"
    Write-Host "5A         / 3.3 mm2       / 2.0 mm   / gruby"
    Write-Host "10A        / 6.7 mm2       / 2.9 mm   / bardzo gruby"
    Write-Host "15A        / 10.0 mm2      / 3.6 mm   / ekstra gruby"
    Write-Host ""
    Write-Host "Info: Uzyj przewodow wielozylowych dla lepszej elastycznosci" -ForegroundColor Blue
}

function Invoke-Calculator {
    Write-Header "KALKULATOR DOBORU TRANSFORMATORA DO PRZECINARKI STYROPINU"
    Write-Host ""
    
    try {
        $dlugosc_drutu = [float](Read-Host "dlugosc drutu [cm]")
        $dlugosc_drutu_m = $dlugosc_drutu / 100
        
        $srednica_drutu = [float](Read-Host "srednica drutu [mm]")
        $opor_na_metrze = [float](Read-Host "opor drutu [ohm/m]")
        $dlugosc_przewodow_dc = [float](Read-Host "dlugosc przewodow DC (zasilacz->drut) [m]")
        
        # Obliczenia podstawowe
        $opor_calkowity = $opor_na_metrze * $dlugosc_drutu_m
        $napiecie_optymalne = $opor_calkowity * 3  # Dla pradu ok 3A
        $moc_potrzebna = $napiecie_optymalne * 3
        $prad_obwodu = 3.0  # Zakladamy staly prad
        
        # Zaokraglenie do dostepnych wartosci
        if ($napiecie_optymalne -le 12) {
            $napiecie_zasilacza = 12
        } elseif ($napiecie_optymalne -le 24) {
            $napiecie_zasilacza = 24
        } else {
            $napiecie_zasilacza = 36
        }
        
        $prad_zasilacza = $moc_potrzebna / $napiecie_zasilacza
        $moc_zasilacza = $napiecie_zasilacza * $prad_zasilacza
        
        # Obliczanie temperatury (przyblizone)
        $przekroj_drutu = [Math]::PI * [Math]::Pow($srednica_drutu/2, 2)  # mm2
        $srednica_m = $srednica_drutu / 1000  # m
        $powierzchnia = [Math]::PI * $srednica_m * $dlugosc_drutu_m  # m2
        
        # Gestosc mocy [W/m2]
        if ($powierzchnia -gt 0) {
            $gestosc_mocy = $moc_potrzebna / $powierzchnia
        } else {
            $gestosc_mocy = 0
        }
        
        # Przyblizona temperatura (C)
        if ($gestosc_mocy -gt 0) {
            $temp_roznica = $gestosc_mocy / 15
        } else {
            $temp_roznica = 0
        }
        $temperatura = 20 + $temp_roznica
        
        # Korekta temperatury
        if ($temperatura -gt 800) {
            $temperatura = 800 + ($temperatura - 800) * 0.3
        }
        
        # Ocena temperatury
        if ($temperatura -lt 100) {
            $ocena_temp = "Niska - moze byc za wolna"
            $color_temp = "Green"
        } elseif ($temperatura -lt 300) {
            $ocena_temp = "Srednia - dobra do cienkich materialow"
            $color_temp = "Yellow"
        } elseif ($temperatura -lt 600) {
            $ocena_temp = "Wysoka - optymalna do przecinania"
            $color_temp = "Blue"
        } else {
            $ocena_temp = "Bardzo wysoka - szybkie przecinanie"
            $color_temp = "Red"
        }
        
        # Obliczanie przekroju przewodow zasilajacych
        $wynik = Get-WireSize -current $prad_zasilacza
        $przekroj_zasilajacy = $wynik[0]
        $srednica_zasilajacego = $wynik[1]
        
        # Spadki napiecia w przewodach DC
        $opor_udzialowy_miedzi = 0.017  # ohm/mm2/m
        $opor_przewodu_jednego = ($opor_udzialowy_miedzi * $dlugosc_przewodow_dc) / $przekroj_zasilajacy
        $spadek_napiecia_jeden_przewod = $prad_zasilacza * $opor_przewodu_jednego
        $spadek_napiecia_razem = $spadek_napiecia_jeden_przewod * 2  # Tam i z powrotem
        $spadek_procentowy = ($spadek_napiecia_razem / $napiecie_zasilacza) * 100
        
        # Wyprowadzenie wynikow
        Write-Section "PARAMETRY DRUTU OPOROWEGO"
        Write-Result "Dlugosc drutu" ("{0:F2}" -f $dlugosc_drutu_m) "m"
        Write-Result "Srednica drutu" ("{0:F1}" -f $srednica_drutu) "mm"
        Write-Result "Przekroj drutu" ("{0:F2}" -f $przekroj_drutu) "mm2"
        Write-Result "Opor calkowity drutu" ("{0:F2}" -f $opor_calkowity) "ohm"
        
        Write-Section "PARAMETRY ELEKTRYCZNE"
        Write-Result "Napiecie optymalne" ("{0:F1}" -f $napiecie_optymalne) "V"
        Write-Result "Prad obciazenia" ("{0:F1}" -f $prad_obwodu) "A"
        Write-Result "Moc grzania" ("{0:F1}" -f $moc_potrzebna) "W"
        
        Write-Section "REKOMENDACJA ZASILACZA"
        Write-Result "Zalecane napiecie" $napiecie_zasilacza "V"
        Write-Result "Minimalny prad" ("{0:F1}" -f $prad_zasilacza) "A"
        Write-Result "Minimalna moc" ("{0:F1}" -f $moc_zasilacza) "W"
        
        Write-Section "PARAMETRY TERMICZNE"
        Write-Result "Szacowana temperatura" ("{0:F0}" -f $temperatura) "C"
        Write-Result "Ocena temperatury" $ocena_temp "" $color_temp
        Write-Result "Gestosc mocy" ("{0:F0}" -f $gestosc_mocy) "W/m2"
        
        Write-Section "PRZEWODY ZASILAJACE DC"
        Write-Result "Dlugosc przewodow DC" ("{0:F1}" -f $dlugosc_przewodow_dc) "m"
        Write-Result "Wymagany przekroj" ("{0:F2}" -f $przekroj_zasilajacy) "mm2"
        Write-Result "Minimalna srednica przewodu" ("{0:F1}" -f $srednica_zasilajacego) "mm"
        Write-Result "Opor jednego przewodu" ("{0:F3}" -f $opor_przewodu_jednego) "ohm"
        Write-Result "Spadek napiecia laczenie" ("{0:F2}" -f $spadek_napiecia_razem) "V"
        Write-Result "Spadek procentowy" ("{0:F1}" -f $spadek_procentowy) "procent"
        
        # Ocena spadku napiecia
        if ($spadek_procentowy -gt 5) {
            Write-Host "Uwaga: Duzy spadek napiecia! ($([Math]::Round($spadek_procentowy, 1)) procent)" -ForegroundColor Red
            Write-WarningMsg "Zwieksz przekroj przewodow lub skroc ich dlugosc"
        } elseif ($spadek_procentowy -gt 2) {
            Write-Host "Ostrzezenie: Sredni spadek napiecia ($([Math]::Round($spadek_procentowy, 1)) procent)" -ForegroundColor Yellow
            Write-Host "Info: Rozwaz zwiekszenie przekroju przewodow" -ForegroundColor Blue
        } else {
            Write-Result "Spadek napiecia" "Akceptowalny" "" "Green"
        }
        
        # Rekomendacje przewodow
        Write-Section "REKOMENDACJE PRZEWODOW"
        Write-Host "- Przewody cienkie (np. krokodylki, przewody elektronika)"
        Write-Host "- Przekroj: minimum 0.7 mm2"
        Write-Host "- Przewody srednie (np. cienkie przewody glosnikowe)"
        Write-Host "- Przekroj: minimum 1.3 mm2"
        Write-Host "- Przewody grube (np. grubsze przewody glosnikowe)"
        Write-Host "- Przekroj: minimum 2.0 mm2"
        Write-Host "- Przewody bardzo grube (np. przewody glosnikowe ekstra)"
        Write-Host "- Przekroj: minimum 3.3 mm2"
        
        Write-Host "- Uzyj przewodow wielozylowych"
        Write-Host "- Zastosuj osobne przewody dla PLUS i MINUS"
        Write-Host "- Zabezpiecz obwod bezpiecznikiem"
        Write-Host "- Uzyj zaciskow typu banana lub krokodyli"
        
        # Ogolne rekomendacje
        Write-Section "OGOLNE REKOMENDACJE"
        Write-Host "- Wybierz zasilacz o mocy: $([Math]::Round($moc_zasilacza))W"
        Write-Host "- Zastosuj zasilacz z regulacja napiecia"
        Write-Host "- Uzyj transformatora obnizajacego napiecie"
        Write-Host "- Zastosuj przelacznik do wlaczania drutu"
        
        if ($temperatura -gt 600) {
            Write-WarningMsg "Wysoka temperatura - zapewnij dobra wentylacje!"
        }
        if ($prad_zasilacza -gt 5) {
            Write-WarningMsg "Duzy prad - uzyj grubych przewodow!"
        }
        
        Write-Host "Info: Drut Kanthal potrzebuje chwili na rozgrzanie" -ForegroundColor Blue
        Write-Host "Info: Nie dotykaj drutu podczas pracy!" -ForegroundColor Blue
        
    } catch {
        Write-Host "Blad: Wprowadz poprawne wartosci liczbowe!" -ForegroundColor Red
    }
}

function Show-WireTypes {
    Write-Header "TABELA TYPOWYCH DRUTOW KANTHAL"
    
    Write-Host ""
    Write-Host "KANTHAL A1 - Parametry podstawowe:" -ForegroundColor Cyan
    Write-Host "Srednica / Przekroj / Opor    / Moc@12V / Moc@24V / Temp. rob."
    Write-Host "---------/----------/----------/--------/--------/-----------"
    Write-Host "0.3 mm   / 0.07 mm2 / 18.0ohm/m / 8 W/m  / 32 W/m / 600-800C"
    Write-Host "0.4 mm   / 0.13 mm2 / 10.2ohm/m / 14 W/m / 56 W/m / 550-750C"
    Write-Host "0.5 mm   / 0.20 mm2 / 6.5ohm/m  / 22 W/m / 89 W/m / 500-700C"
    Write-Host "0.6 mm   / 0.28 mm2 / 4.5ohm/m  / 32 W/m / 128 W/m/ 450-650C"
    Write-Host "0.8 mm   / 0.50 mm2 / 2.6ohm/m  / 55 W/m / 221 W/m/ 400-600C"
    Write-Host "1.0 mm   / 0.79 mm2 / 1.71ohm/m / 84 W/m / 337 W/m/ 350-550C"
    
    Write-Host ""
    Write-Host "INNE MATERIALY:" -ForegroundColor Cyan
    Write-Host "Material    / Opor [ohm/m] dla 1mm / Uwagi"
    Write-Host "------------/-------------------/-------"
    Write-Host "Miedz       / 0.017             / Nie do przecinania!"
    Write-Host "Nichrom     / 1.0-1.5           / Alternatywa"
    Write-Host "Stal        / 0.1-0.2           / Krotkotrwale uzycie"
    
    Write-Section "TABELA PRZEKROJOW PRZEWODOW"
    Show-WireTable
}

function Show-Examples {
    Write-Header "PRZYKLADOWE OBLICZENIA"
    
    Write-Host ""
    Write-Host "PRZYKLAD 1: Drut 150cm, Kanthal 1.0mm (1.71ohm/m), przewody 1m" -ForegroundColor Cyan
    Write-Host "- Opor calkowity drutu: 1.71 x 1.5 = 2.57ohm"
    Write-Host "- Napiecie optymalne: 2.57 x 3A = 7.7V -> Zasilacz 12V"
    Write-Host "- Moc: 12V x 3A = 36W"
    Write-Host "- Temperatura: ~450C"
    Write-Host "- Zasilacz: 12V/3A (36W)"
    Write-Host "- Przewody DC (1m): przekroj 2.0mm2, srednica 1.6mm"
    Write-Host "- Spadek napiecia: ~0.3V (2.5 procent)"
    
    Write-Host ""
    Write-Host "PRZYKLAD 2: Drut 100cm, Kanthal 0.8mm (2.6ohm/m), przewody 2m" -ForegroundColor Cyan
    Write-Host "- Opor calkowity drutu: 2.6 x 1.0 = 2.6ohm"
    Write-Host "- Napiecie optymalne: 2.6 x 3A = 7.8V -> Zasilacz 12V"
    Write-Host "- Moc: 12V x 3A = 36W"
    Write-Host "- Temperatura: ~500C"
    Write-Host "- Zasilacz: 12V/3A (36W)"
    Write-Host "- Przewody DC (2m): przekroj 2.0mm2, srednica 1.6mm"
    Write-Host "- Spadek napiecia: ~0.6V (5 procent)"
    
    Write-Host ""
    Write-Host "PRZYKLAD 3: Drut 80cm, Kanthal 0.5mm (6.5ohm/m), przewody 0.5m" -ForegroundColor Cyan
    Write-Host "- Opor calkowity drutu: 6.5 x 0.8 = 5.2ohm"
    Write-Host "- Napiecie optymalne: 5.2 x 3A = 15.6V -> Zasilacz 24V"
    Write-Host "- Moc: 24V x 3A = 72W"
    Write-Host "- Temperatura: ~650C"
    Write-Host "- Zasilacz: 24V/3A (72W)"
    Write-Host "- Przewody DC (0.5m): przekroj 3.3mm2, srednica 2.0mm"
    Write-Host "- Spadek napiecia: ~0.3V (1.2 procent)"
}

function Show-MainMenu {
    Clear-Screen
    Write-Header "MENU GLOWNE"
    Write-Host ""
    Write-Host "  1. Kalkulator transformatora" -ForegroundColor Green
    Write-Host "  2. Tabela typowych drutow" -ForegroundColor Green
    Write-Host "  3. Przykladowe obliczenia" -ForegroundColor Green
    Write-Host "  4. Wyjscie" -ForegroundColor Red
    Write-Host ""
}

# Glowna petla programu
do {
    Show-MainMenu
    $wybor = Read-Host "Wybierz opcje (1-4)"
    
    switch ($wybor) {
        "1" { 
            Clear-Screen
            Invoke-Calculator
            Write-Host ""
            Read-Host "Nacisnij Enter, aby kontynuowac..."
        }
        "2" { 
            Clear-Screen
            Show-WireTypes
            Read-Host "Nacisnij Enter, aby kontynuowac..."
        }
        "3" { 
            Clear-Screen
            Show-Examples
            Read-Host "Nacisnij Enter, aby kontynuowac..."
        }
        "4" { 
            Clear-Screen
            Write-Header "DO WIDZENIA!"
            Write-Host "Dziekujemy za skorzystanie z kalkulatora!" -ForegroundColor Green
        }
        default { 
            Write-Host "Blad: Nieprawidlowy wybor!" -ForegroundColor Red
            Read-Host "Nacisnij Enter, aby kontynuowac..."
        }
    }
} while ($wybor -ne "4")
