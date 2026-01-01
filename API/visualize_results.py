# ============================================================
# VİZUALİZASYON KODU - TEZ İÇİN GRAFİKLER
# ============================================================

import matplotlib.pyplot as plt
import numpy as np

# Türkçe karakter desteği
plt.rcParams['font.family'] = 'DejaVu Sans'

# ============================================================
# GRAFİK 1: SKOR KARŞILAŞTIRMA (Çizgi Grafik)
# ============================================================

def plot_score_comparison():
    """
    Tablo 5.1: Top 5 Aday için algoritma skorları
    """
    # Test verisi (test sonuçlarından)
    ranks = ['1', '2', '3', '4', '5']
    basit = [86.1, 36.1, 38.9, 22.2, 30.6]
    bm25 = [100.0, 34.4, 21.9, 22.7, 14.7]
    hybrid = [95.8, 34.9, 27.0, 22.5, 19.5]
    
    plt.figure(figsize=(10, 6))
    
    x = np.arange(len(ranks))
    
    plt.plot(x, basit, marker='o', linewidth=2, markersize=8, 
             label='Basit Kesisim', color='#3498db')
    plt.plot(x, bm25, marker='s', linewidth=2, markersize=8, 
             label='BM25 (Min-Max)', color='#e74c3c')
    plt.plot(x, hybrid, marker='^', linewidth=3, markersize=10, 
             label='Hybrid Scoring', color='#2ecc71')
    
    plt.xlabel('Aday Siralamasi', fontsize=12, fontweight='bold')
    plt.ylabel('Eslesme Skoru (%)', fontsize=12, fontweight='bold')
    plt.title('Algoritma Karsilastirmasi - Top 5 Aday', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.xticks(x, ranks)
    plt.ylim(0, 105)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=11, loc='upper right')
    
    # Değerleri noktalara ekle
    for i, v in enumerate(hybrid):
        plt.text(i, v + 3, f'{v}%', ha='center', fontsize=9, 
                fontweight='bold', color='#2ecc71')
    
    plt.tight_layout()
    plt.savefig('grafik_1_skor_karsilastirma.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 1 kaydedildi: grafik_1_skor_karsilastirma.png")
    plt.close()


# ============================================================
# GRAFİK 2: SIFIR SKOR ANALİZİ (Bar Chart)
# ============================================================

def plot_zero_score_analysis():
    """
    Tablo 5.2: Sıfır skor analizi
    """
    algorithms = ['Basit\nKesisim', 'BM25\n(Min-Max)', 'Hybrid\nScoring']
    zero_scores = [0, 1, 0]  # Test sonuçlarından
    total = 10
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    bars = ax.bar(algorithms, zero_scores, color=colors, alpha=0.7, 
                   edgecolor='black', linewidth=1.5)
    
    # Değerleri bar'ların üstüne ekle
    for i, (bar, val) in enumerate(zip(bars, zero_scores)):
        height = bar.get_height()
        percentage = (val / total) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{val}/{total}\n({percentage:.0f}%)',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Checkmark veya X işareti ekle
        if val == 0:
            ax.text(bar.get_x() + bar.get_width()/2., -0.3,
                   '✓ COZULDU', ha='center', fontsize=10, 
                   color='green', fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2., -0.3,
                   '✗ SORUN', ha='center', fontsize=10, 
                   color='red', fontweight='bold')
    
    ax.set_ylabel('Sifir Skor Alan Aday Sayisi', fontsize=12, fontweight='bold')
    ax.set_title('Sifir Skor Problemi Analizi', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, max(zero_scores) + 1)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('grafik_2_sifir_skor.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 2 kaydedildi: grafik_2_sifir_skor.png")
    plt.close()


# ============================================================
# GRAFİK 3: PERFORMANS KARŞILAŞTIRMA (Bar Chart)
# ============================================================

def plot_performance_comparison():
    """
    Tablo 5.3: Performans karşılaştırması
    """
    algorithms = ['Basit\nKesisim', 'BM25', 'Hybrid']
    times = [0.02, 2.51, 2.47]  # ms
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    bars = ax.bar(algorithms, times, color=colors, alpha=0.7,
                   edgecolor='black', linewidth=1.5)
    
    # Değerleri bar'ların üstüne ekle
    for bar, val in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{val:.2f} ms', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
    
    # En hızlı işareti
    ax.text(bars[0].get_x() + bars[0].get_width()/2., -0.15,
           '⚡ EN HIZLI', ha='center', fontsize=10, 
           color='blue', fontweight='bold')
    
    ax.set_ylabel('Ortalama Yanit Suresi (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Performans Karsilastirmasi', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, max(times) + 0.5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('grafik_3_performans.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 3 kaydedildi: grafik_3_performans.png")
    plt.close()


# ============================================================
# GRAFİK 4: SKOR DAĞILIMI (Box Plot)
# ============================================================

def plot_score_distribution():
    """
    Tablo 5.4: Skor dağılımı - Box Plot
    """
    # Test sonuçlarından tüm skorlar
    basit_all = [86.1, 36.1, 38.9, 22.2, 30.6, 16.7, 19.4, 13.9, 13.9, 8.3]
    bm25_all = [100.0, 34.4, 21.9, 22.7, 14.7, 11.5, 10.0, 3.6, 3.6, 0.0]
    hybrid_all = [95.8, 34.9, 27.0, 22.5, 19.5, 13.0, 12.8, 6.7, 6.7, 2.5]
    
    data = [basit_all, bm25_all, hybrid_all]
    labels = ['Basit\nKesisim', 'BM25', 'Hybrid']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bp = ax.boxplot(data, labels=labels, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))
    
    # Renkleri değiştir
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax.set_ylabel('Eslesme Skoru (%)', fontsize=12, fontweight='bold')
    ax.set_title('Skor Dagilimi (Box Plot)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # İstatistikleri ekle
    for i, (d, label) in enumerate(zip(data, labels), 1):
        median = np.median(d)
        mean = np.mean(d)
        ax.text(i, -8, f'Ort: {mean:.1f}%\nMed: {median:.1f}%', 
               ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('grafik_4_dagilim.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 4 kaydedildi: grafik_4_dagilim.png")
    plt.close()


# ============================================================
# GRAFİK 5: HYBRID DETAY (Stacked Bar)
# ============================================================

def plot_hybrid_breakdown():
    """
    Hybrid skorun bileşenlerini göster (BM25 vs Basit)
    """
    ranks = ['Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']
    
    # BM25 katkısı (%70)
    bm25_contribution = [
        0.7 * 100.0,  # Rank 1
        0.7 * 34.4,   # Rank 2
        0.7 * 21.9,   # Rank 3
        0.7 * 22.7,   # Rank 4
        0.7 * 14.7    # Rank 5
    ]
    
    # Basit kesişim katkısı (%30)
    simple_contribution = [
        0.3 * 86.1,   # Rank 1
        0.3 * 36.1,   # Rank 2
        0.3 * 38.9,   # Rank 3
        0.3 * 22.2,   # Rank 4
        0.3 * 30.6    # Rank 5
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(ranks))
    width = 0.5
    
    p1 = ax.bar(x, bm25_contribution, width, label='BM25 Katkisi (70%)',
                color='#e74c3c', alpha=0.8)
    p2 = ax.bar(x, simple_contribution, width, bottom=bm25_contribution,
                label='Basit Kesisim Katkisi (30%)', color='#3498db', alpha=0.8)
    
    ax.set_ylabel('Skor Bileseni (%)', fontsize=12, fontweight='bold')
    ax.set_title('Hybrid Scoring Bilesenleri', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(ranks)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Toplam skorları ekle
    totals = [b + s for b, s in zip(bm25_contribution, simple_contribution)]
    for i, total in enumerate(totals):
        ax.text(i, total + 2, f'{total:.1f}%', ha='center', 
               fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('grafik_5_hybrid_detay.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 5 kaydedildi: grafik_5_hybrid_detay.png")
    plt.close()


# ============================================================
# GRAFİK 6: HEATMAP (Tüm Adaylar)
# ============================================================

def plot_heatmap():
    """
    Tüm adaylar için algoritma skorları - Heatmap
    """
    import matplotlib.patches as mpatches
    
    # Test sonuçlarından
    user_ids = ['82', '51', '50', '46', '52', '48', '47', '45', '49', '44']
    
    # Skorlar (Basit, BM25, Hybrid)
    scores = np.array([
        [86.1, 100.0, 95.8],  # 82
        [36.1, 34.4, 34.9],   # 51
        [38.9, 21.9, 27.0],   # 50
        [22.2, 22.7, 22.5],   # 46
        [30.6, 14.7, 19.5],   # 52
        [16.7, 11.5, 13.0],   # 48
        [19.4, 10.0, 12.8],   # 47
        [13.9, 3.6, 6.7],     # 45
        [13.9, 3.6, 6.7],     # 49
        [8.3, 0.0, 2.5]       # 44
    ])
    
    fig, ax = plt.subplots(figsize=(8, 10))
    
    im = ax.imshow(scores, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    # Eksen etiketleri
    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(len(user_ids)))
    ax.set_xticklabels(['Basit', 'BM25', 'Hybrid'], fontsize=11)
    ax.set_yticklabels([f'UserID {uid}' for uid in user_ids], fontsize=10)
    
    # Değerleri hücrelere ekle
    for i in range(len(user_ids)):
        for j in range(3):
            text = ax.text(j, i, f'{scores[i, j]:.1f}%',
                          ha="center", va="center", color="black", 
                          fontsize=9, fontweight='bold')
    
    ax.set_title('Tum Adaylar icin Algoritma Skorlari', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Eslesme Skoru (%)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('grafik_6_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik 6 kaydedildi: grafik_6_heatmap.png")
    plt.close()


# ============================================================
# TÜM GRAFİKLERİ OLUŞTUR
# ============================================================

def create_all_plots():
    """Tüm grafikleri oluştur"""
    print("\n" + "="*60)
    print(" "*15 + "GRAFİK OLUŞTURMA BAŞLIYOR")
    print("="*60 + "\n")
    
    plot_score_comparison()
    plot_zero_score_analysis()
    plot_performance_comparison()
    plot_score_distribution()
    plot_hybrid_breakdown()
    plot_heatmap()
    
    print("\n" + "="*60)
    print(" "*10 + "TÜM GRAFİKLER BAŞARIYLA OLUŞTURULDU! ✅")
    print("="*60)
    print("\nOluşturulan dosyalar:")
    print("  1. grafik_1_skor_karsilastirma.png")
    print("  2. grafik_2_sifir_skor.png")
    print("  3. grafik_3_performans.png")
    print("  4. grafik_4_dagilim.png")
    print("  5. grafik_5_hybrid_detay.png")
    print("  6. grafik_6_heatmap.png")
    print("\nBu dosyaları tezinize ekleyebilirsiniz!\n")


if __name__ == "__main__":
    create_all_plots()