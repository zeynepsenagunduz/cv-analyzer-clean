# ============================================================
# TEST SONUÇLARINI TABLO HALİNDE GÖSTER
# ============================================================

from prettytable import PrettyTable

# ============================================================
# TABLO 1: ALGORİTMA KARŞILAŞTIRMASI
# ============================================================

def table_algorithm_comparison():
    """Tablo 5.1: Algoritma Karşılaştırması"""
    
    table = PrettyTable()
    table.field_names = ["Rank", "UserID", "Ortak Beceri", "Basit", "BM25", "Hybrid", "Analiz"]
    
    # Test sonuçlarından
    table.add_row([1, 82, "31/36", "86.1%", "100.0%", "95.8%", "Mükemmel eşleşme"])
    table.add_row([2, 51, "13/36", "36.1%", "34.4%", "34.9%", "İyi eşleşme"])
    table.add_row([3, 50, "14/36", "38.9%", "21.9%", "27.0%", "Orta eşleşme"])
    table.add_row([4, 46, "8/36", "22.2%", "22.7%", "22.5%", "Orta-zayıf"])
    table.add_row([5, 52, "11/36", "30.6%", "14.7%", "19.5%", "Zayıf eşleşme"])
    
    table.align = "l"
    table.align["Rank"] = "c"
    table.align["Basit"] = "r"
    table.align["BM25"] = "r"
    table.align["Hybrid"] = "r"
    
    print("\n" + "="*90)
    print("TABLO 5.1: ALGORİTMA KARŞILAŞTIRMASI (Top 5 Aday)")
    print("="*90)
    print(table)
    
    return table


# ============================================================
# TABLO 2: SIFIR SKOR ANALİZİ
# ============================================================

def table_zero_score_analysis():
    """Tablo 5.2: Sıfır Skor Analizi"""
    
    table = PrettyTable()
    table.field_names = ["Algoritma", "Toplam Aday", "Sıfır Skor Alan", "Sıfır Oranı", "Durum"]
    
    table.add_row(["Basit Kesişim", 10, 0, "0%", "✓"])
    table.add_row(["BM25 (Min-Max)", 10, 1, "10%", "✗ SORUN"])
    table.add_row(["Hybrid Scoring", 10, 0, "0%", "✓ ÇÖZÜLDÜ"])
    
    table.align = "l"
    table.align["Toplam Aday"] = "c"
    table.align["Sıfır Skor Alan"] = "c"
    table.align["Sıfır Oranı"] = "c"
    
    print("\n" + "="*90)
    print("TABLO 5.2: SIFIR SKOR ANALİZİ")
    print("="*90)
    print(table)
    
    return table


# ============================================================
# TABLO 3: PERFORMANS KARŞILAŞTIRMASI
# ============================================================

def table_performance():
    """Tablo 5.3: Performans Karşılaştırması"""
    
    table = PrettyTable()
    table.field_names = ["Algoritma", "Ortalama Süre", "Hız Karşılaştırması"]
    
    table.add_row(["Basit Kesişim", "0.02 ms", "En Hızlı ⚡ (baseline)"])
    table.add_row(["BM25 (Min-Max)", "2.51 ms", "164.3x daha yavaş"])
    table.add_row(["Hybrid Scoring", "2.47 ms", "161.4x daha yavaş"])
    
    table.align = "l"
    table.align["Ortalama Süre"] = "r"
    
    print("\n" + "="*90)
    print("TABLO 5.3: PERFORMANS KARŞILAŞTIRMASI")
    print("="*90)
    print(table)
    print("\nYorum: Hybrid, BM25'den sadece %1.8 daha yavaş (2.47ms vs 2.51ms)")
    
    return table


# ============================================================
# TABLO 4: İSTATİSTİKSEL ÖZET
# ============================================================

def table_statistics():
    """Tablo 5.4: İstatistiksel Özet"""
    
    table = PrettyTable()
    table.field_names = ["Algoritma", "Ortalama", "Min", "Max", "Std Dev"]
    
    table.add_row(["Basit Kesişim", "28.6%", "8.3%", "86.1%", "Yüksek"])
    table.add_row(["BM25 (Min-Max)", "22.2%", "0.0%", "100.0%", "Çok Yüksek"])
    table.add_row(["Hybrid Scoring", "24.1%", "2.5%", "95.8%", "Dengeli"])
    
    table.align = "l"
    table.align["Ortalama"] = "r"
    table.align["Min"] = "r"
    table.align["Max"] = "r"
    
    print("\n" + "="*90)
    print("TABLO 5.4: İSTATİSTİKSEL ÖZET")
    print("="*90)
    print(table)
    
    return table


# ============================================================
# TABLO 5: TÜM ADAYLAR İÇİN DETAYLI SKORLAR
# ============================================================

def table_all_candidates():
    """Tablo 5.5: Tüm Adaylar için Detaylı Skorlar"""
    
    table = PrettyTable()
    table.field_names = ["Rank", "UserID", "Ortak", "Basit", "BM25", "Hybrid"]
    
    # Tüm test sonuçları
    data = [
        [1, 82, "31/36", "86.1%", "100.0%", "95.8%"],
        [2, 51, "13/36", "36.1%", "34.4%", "34.9%"],
        [3, 50, "14/36", "38.9%", "21.9%", "27.0%"],
        [4, 46, "8/36", "22.2%", "22.7%", "22.5%"],
        [5, 52, "11/36", "30.6%", "14.7%", "19.5%"],
        [6, 48, "6/36", "16.7%", "11.5%", "13.0%"],
        [7, 47, "7/36", "19.4%", "10.0%", "12.8%"],
        [8, 45, "5/36", "13.9%", "3.6%", "6.7%"],
        [9, 49, "5/36", "13.9%", "3.6%", "6.7%"],
        [10, 44, "3/36", "8.3%", "0.0%", "2.5%"],
    ]
    
    for row in data:
        table.add_row(row)
    
    table.align = "c"
    table.align["Basit"] = "r"
    table.align["BM25"] = "r"
    table.align["Hybrid"] = "r"
    
    print("\n" + "="*90)
    print("TABLO 5.5: TÜM ADAYLAR İÇİN DETAYLI SKORLAR")
    print("="*90)
    print(table)
    
    return table


# ============================================================
# TÜM TABLOLARI GÖSTER
# ============================================================

def show_all_tables():
    """Tüm tabloları sırayla göster"""
    
    print("\n")
    print("╔" + "="*88 + "╗")
    print("║" + " "*25 + "TEZ RAPORU - TEST SONUÇLARI TABLOLARI" + " "*26 + "║")
    print("╚" + "="*88 + "╝")
    
    table_algorithm_comparison()
    table_zero_score_analysis()
    table_performance()
    table_statistics()
    table_all_candidates()
    
    print("\n" + "="*90)
    print(" "*25 + "TÜM TABLOLAR GÖSTERILDI ✅")
    print("="*90)
    print("\nBu tabloları tez raporunuza kopyalayabilirsiniz.")
    print("(Terminal çıktısını kopyala-yapıştır yapabilirsiniz)\n")




# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    show_all_tables()
    
   