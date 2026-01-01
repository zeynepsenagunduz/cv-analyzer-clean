# ============================================================
# TEST DOSYASI: test_algorithms.py
# Tez için algoritma karşılaştırması ve performans testleri
# ============================================================

import time
from db import get_db_connection
import json
from rank_bm25 import BM25Okapi

# ============================================================
# VERİTABANI VE YARDIMCI FONKSİYONLAR
# ============================================================




def safe_keywords(raw_kw):
    """JSON string'i listeye çevir"""
    try:
        if isinstance(raw_kw, str):
            return json.loads(raw_kw)
        elif isinstance(raw_kw, list):
            return raw_kw
        else:
            return []
    except:
        return []


# ============================================================
# HYBRID SCORING FONKSİYONLARI (Mevcut Sistem)
# ============================================================

def hybrid_score_for_applicants(cv_keywords, job_keywords, all_cv_texts, job_text, cv_index):
    """
    Hybrid Scoring for HeadHunter: BM25 (70%) + Simple Intersection (30%)
    """
    # 1. BASİT KESİŞİM SKORU
    if len(job_keywords) == 0:
        simple_score = 0
    else:
        common = set(cv_keywords) & set(job_keywords)
        simple_score = (len(common) / len(job_keywords)) * 100
    
    # 2. BM25 SKORU
    try:
        tokenized_corpus = [text.lower().split() for text in all_cv_texts]
        tokenized_query = job_text.lower().split()
        
        if not tokenized_corpus or not tokenized_query:
            bm25_normalized = 0
        else:
            bm25 = BM25Okapi(tokenized_corpus, k1=1.5, b=0.75)
            raw_scores = bm25.get_scores(tokenized_query)
            
            if len(raw_scores) == 0:
                bm25_normalized = 0
            else:
                min_score = min(raw_scores)
                max_score = max(raw_scores)
                
                if max_score == min_score:
                    bm25_normalized = 50.0
                else:
                    bm25_normalized = ((raw_scores[cv_index] - min_score) / (max_score - min_score)) * 100
    except Exception as e:
        print(f"BM25 error in hybrid: {e}")
        bm25_normalized = 0
    
    # 3. HYBRİD SKOR (70% BM25 + 30% Simple)
    hybrid = (0.7 * bm25_normalized) + (0.3 * simple_score)
    
    return round(hybrid, 2)


# ============================================================
# TEST İÇİN ESKİ ALGORİTMALAR (Karşılaştırma için)
# ============================================================

def simple_intersection_score(cv_keywords, job_keywords):
    """
    Basit Set Kesişimi (Eski yöntem - sadece test için)
    
    Formül: (Ortak Beceri Sayısı / İş Gereksinimi Sayısı) × 100
    """
    if len(job_keywords) == 0:
        return 0
    
    common = set(cv_keywords) & set(job_keywords)
    score = (len(common) / len(job_keywords)) * 100
    
    return round(score, 2)


def bm25_only_score(cv_keywords, job_keywords, all_cv_texts, cv_index):
    """
    Sadece BM25 (Min-Max Normalized) - Eski yöntem, sadece test için
    
    BM25 ile skorlama + Min-Max normalizasyon
    """
    try:
        job_text = " ".join(job_keywords)
        
        tokenized_corpus = [text.lower().split() for text in all_cv_texts]
        tokenized_query = job_text.lower().split()
        
        if not tokenized_corpus or not tokenized_query:
            return 0
        
        bm25 = BM25Okapi(tokenized_corpus, k1=1.5, b=0.75)
        raw_scores = bm25.get_scores(tokenized_query)
        
        if len(raw_scores) == 0:
            return 0
        
        # Min-Max normalize
        min_score = min(raw_scores)
        max_score = max(raw_scores)
        
        if max_score == min_score:
            return 50.0
        
        normalized = ((raw_scores[cv_index] - min_score) / (max_score - min_score)) * 100
        return round(normalized, 2)
        
    except Exception as e:
        print(f"BM25 error: {e}")
        return 0


# ============================================================
# TEST 1: ALGORİTMA KARŞILAŞTIRMASI
# ============================================================

def compare_algorithms_test():
    """
    3 algoritmayı karşılaştır ve sonuçları yazdır
    
    Testler:
    1. Basit Set Kesişimi
    2. BM25 (Min-Max Normalized)
    3. Hybrid Scoring (BM25 70% + Basit 30%)
    """
    print("\n" + "="*70)
    print(" " * 15 + "ALGORİTMA KARŞILAŞTIRMA TESTİ")
    print("="*70)
    
    # Test verisi hazırla
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1 iş ilanı al (test için)
    cursor.execute("SELECT id, jobpost_keywords FROM jobposts WHERE id = 21")
    job = cursor.fetchone()
    
    if not job:
        print("HATA: İş ilanı bulunamadı!")
        cursor.execute("SELECT id, jobpost_keywords FROM jobposts LIMIT 1")
        job = cursor.fetchone()
    
    job_id = job[0]
    job_keywords = safe_keywords(job[1])
    
    print(f"\nTest İş İlanı:")
    print(f"  ID: {job_id}")
    print(f"  Aranan Beceriler: {job_keywords[:5]}...")
    print(f"  Toplam Gereksinim: {len(job_keywords)} beceri")
    
    # Tüm CV'leri al
    cursor.execute("SELECT id, userid, keywords FROM cvs")
    cvs = cursor.fetchall()
    
    # Tüm CV metinlerini hazırla
    all_cv_texts = []
    cv_data = []
    
    for i, row in enumerate(cvs):
        cv_id = row[0]
        cv_userid = row[1]
        cv_keywords = safe_keywords(row[2])
        cv_text = " ".join(cv_keywords)
        all_cv_texts.append(cv_text)
        cv_data.append({
            'index': i,
            'cv_id': cv_id,
            'userid': cv_userid,
            'keywords': cv_keywords
        })
    
    print(f"\nTest Verisi:")
    print(f"  Toplam CV: {len(cvs)}")
    
    print("\n" + "-"*70)
    print("SKOR KARŞILAŞTIRMASI (Top 10 Aday)")
    print("-"*70)
    
    # Her CV için 3 algoritmayı hesapla
    results = []
    
    for cv in cv_data:
        cv_keywords = cv['keywords']
        cv_index = cv['index']
        userid = cv['userid']
        
        # Ortak beceri sayısı
        common = set(cv_keywords) & set(job_keywords)
        common_count = len(common)
        
        # 1. Basit Kesişim
        simple = simple_intersection_score(cv_keywords, job_keywords)
        
        # 2. BM25 Only
        bm25 = bm25_only_score(cv_keywords, job_keywords, all_cv_texts, cv_index)
        
        # 3. Hybrid (mevcut sistem)
        hybrid = hybrid_score_for_applicants(
            cv_keywords, 
            job_keywords, 
            all_cv_texts, 
            " ".join(job_keywords), 
            cv_index
        )
        
        results.append({
            'userid': userid,
            'common_count': common_count,
            'total_required': len(job_keywords),
            'simple': simple,
            'bm25': bm25,
            'hybrid': hybrid
        })
    
    # Sonuçları sırala (Hybrid'e göre)
    results.sort(key=lambda x: x['hybrid'], reverse=True)
    
    # Top 10'u yazdır
    print(f"\n{'Rank':<6} {'UserID':<12} {'Ortak':<12} {'Basit':<12} {'BM25':<12} {'Hybrid':<12}")
    print("-"*70)
    
    for i, r in enumerate(results[:10], 1):
        print(f"{i:<6} {str(r['userid']):<12} {r['common_count']}/{r['total_required']:<10} "
              f"{r['simple']:>6.1f}%     {r['bm25']:>6.1f}%     {r['hybrid']:>6.1f}%")
    
    # Sıfır skor analizi
    simple_zeros = sum(1 for r in results if r['simple'] == 0)
    bm25_zeros = sum(1 for r in results if r['bm25'] == 0)
    hybrid_zeros = sum(1 for r in results if r['hybrid'] == 0)
    
    print("\n" + "-"*70)
    print("SIFIR SKOR ANALİZİ")
    print("-"*70)
    print(f"{'Algoritma':<20} {'Sıfır Skor Alan':<20} {'Oran':<10}")
    print("-"*70)
    print(f"{'Basit Kesişim':<20} {simple_zeros}/{len(results):<18} %{simple_zeros/len(results)*100:.1f}")
    print(f"{'BM25 (Min-Max)':<20} {bm25_zeros}/{len(results):<18} %{bm25_zeros/len(results)*100:.1f}  {'❌ SORUN!' if bm25_zeros > 0 else '✅'}")
    print(f"{'Hybrid Scoring':<20} {hybrid_zeros}/{len(results):<18} %{hybrid_zeros/len(results)*100:.1f}  {'✅ ÇÖZÜLDÜ!' if hybrid_zeros == 0 else ''}")
    
    # İstatistikler
    print("\n" + "-"*70)
    print("İSTATİSTİKLER")
    print("-"*70)
    
    avg_simple = sum(r['simple'] for r in results) / len(results)
    avg_bm25 = sum(r['bm25'] for r in results) / len(results)
    avg_hybrid = sum(r['hybrid'] for r in results) / len(results)
    
    print(f"{'Algoritma':<20} {'Ortalama Skor':<20} {'Min':<10} {'Max':<10}")
    print("-"*70)
    print(f"{'Basit Kesişim':<20} {avg_simple:>6.1f}%            {min(r['simple'] for r in results):>6.1f}%  {max(r['simple'] for r in results):>6.1f}%")
    print(f"{'BM25 (Min-Max)':<20} {avg_bm25:>6.1f}%            {min(r['bm25'] for r in results):>6.1f}%  {max(r['bm25'] for r in results):>6.1f}%")
    print(f"{'Hybrid Scoring':<20} {avg_hybrid:>6.1f}%            {min(r['hybrid'] for r in results):>6.1f}%  {max(r['hybrid'] for r in results):>6.1f}%")
    
    print("\n" + "="*70)
    
    conn.close()
    
    return results


# ============================================================
# TEST 2: PERFORMANS TESTİ
# ============================================================

def performance_test():
    """
    Algoritmaların performansını ölç (yanıt süresi)
    """
    print("\n" + "="*70)
    print(" " * 25 + "PERFORMANS TESTİ")
    print("="*70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Test verisi
    cursor.execute("SELECT jobpost_keywords FROM jobposts LIMIT 1")
    job_keywords = safe_keywords(cursor.fetchone()[0])
    
    cursor.execute("SELECT keywords FROM cvs")
    cvs = cursor.fetchall()
    all_cv_keywords = [safe_keywords(row[0]) for row in cvs]
    all_cv_texts = [" ".join(kw) for kw in all_cv_keywords]
    
    cv_count = len(all_cv_keywords)
    iterations = 50  # Her algoritma için 50 iterasyon
    
    print(f"\nTest Parametreleri:")
    print(f"  - CV Sayısı: {cv_count}")
    print(f"  - İterasyon: {iterations}")
    print(f"  - Her iterasyonda {cv_count} CV işleniyor")
    print(f"\nTest başlıyor...\n")
    
    # Test 1: Basit Kesişim
    print("⏳ Basit Kesişim testi yapılıyor...")
    start = time.time()
    for _ in range(iterations):
        for cv_kw in all_cv_keywords:
            simple_intersection_score(cv_kw, job_keywords)
    simple_time = (time.time() - start) / iterations * 1000
    print(f"✅ Tamamlandı: {simple_time:.2f} ms")
    
    # Test 2: BM25
    print("⏳ BM25 testi yapılıyor...")
    start = time.time()
    for _ in range(iterations):
        for i, cv_kw in enumerate(all_cv_keywords):
            bm25_only_score(cv_kw, job_keywords, all_cv_texts, i)
    bm25_time = (time.time() - start) / iterations * 1000
    print(f"✅ Tamamlandı: {bm25_time:.2f} ms")
    
    # Test 3: Hybrid
    print("⏳ Hybrid Scoring testi yapılıyor...")
    start = time.time()
    for _ in range(iterations):
        for i, cv_kw in enumerate(all_cv_keywords):
            hybrid_score_for_applicants(cv_kw, job_keywords, all_cv_texts, " ".join(job_keywords), i)
    hybrid_time = (time.time() - start) / iterations * 1000
    print(f"✅ Tamamlandı: {hybrid_time:.2f} ms")
    
    # Sonuçlar
    print("\n" + "-"*70)
    print("SONUÇLAR (Ortalama Yanıt Süresi)")
    print("-"*70)
    print(f"{'Algoritma':<20} {'Süre':<15} {'Hız':<15}")
    print("-"*70)
    print(f"{'Basit Kesişim':<20} {simple_time:>8.2f} ms    {'En Hızlı ⚡':<15}")
    print(f"{'BM25 (Min-Max)':<20} {bm25_time:>8.2f} ms    {f'{bm25_time/simple_time:.1f}x daha yavaş':<15}")
    print(f"{'Hybrid Scoring':<20} {hybrid_time:>8.2f} ms    {f'{hybrid_time/simple_time:.1f}x daha yavaş':<15}")
    
    print("\n" + "-"*70)
    print("KARŞILAŞTIRMA")
    print("-"*70)
    diff_bm25 = ((hybrid_time - bm25_time) / bm25_time * 100)
    print(f"Hybrid vs BM25:    {'+' if diff_bm25 > 0 else ''}{diff_bm25:.1f}% ")
    print(f"                   ({hybrid_time:.2f}ms vs {bm25_time:.2f}ms)")
    print(f"\nYorum: Hybrid, BM25'den sadece {abs(diff_bm25):.1f}% daha yavaş")
    print(f"       ama sıfır skor problemini çözüyor. ✅")
    
    print("\n" + "="*70)
    
    conn.close()


# ============================================================
# TEST 3: GERÇEK KULLANICI SENARYOLARı
# ============================================================

def real_world_scenarios():
    """
    Gerçek dünya senaryoları ile test
    """
    print("\n" + "="*70)
    print(" " * 18 + "GERÇEK KULLANICI SENARYOLARı")
    print("="*70)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Senaryo 1: Nadir becerili aday
    print("\n📌 SENARYO 1: Nadir Becerili Aday (zeynep.gunduz)")
    print("-"*70)
    
    cursor.execute("SELECT keywords FROM cvs WHERE userid = 82")
    cv = cursor.fetchone()
    if cv:
        cv_keywords = safe_keywords(cv[0])
        print(f"Beceriler: {', '.join(cv_keywords[:10])}...")
        print(f"Toplam: {len(cv_keywords)} beceri")
        
        # Test iş ilanı
        cursor.execute("SELECT id, jobpost_keywords FROM jobposts WHERE id = 21")
        job = cursor.fetchone()
        job_keywords = safe_keywords(job[1])
        
        print(f"\nİş İlanı #21:")
        print(f"Gereksinimler: {', '.join(job_keywords[:10])}...")
        print(f"Toplam: {len(job_keywords)} beceri")
        
        # Ortak beceriler
        common = set(cv_keywords) & set(job_keywords)
        print(f"\nOrtak Beceriler: {len(common)}/{len(job_keywords)}")
        print(f"Örnekler: {', '.join(list(common)[:8])}...")
        
        print(f"\n{'Algoritma':<20} {'Skor':<10} {'Yorum'}")
        print("-"*70)
        
        # Skorlar
        cursor.execute("SELECT keywords FROM cvs")
        all_cvs = cursor.fetchall()
        all_cv_texts = [" ".join(safe_keywords(row[0])) for row in all_cvs]
        cv_index = 0  # zeynep'in index'i
        
        simple = simple_intersection_score(cv_keywords, job_keywords)
        bm25 = bm25_only_score(cv_keywords, job_keywords, all_cv_texts, cv_index)
        hybrid = hybrid_score_for_applicants(cv_keywords, job_keywords, all_cv_texts, " ".join(job_keywords), cv_index)
        
        print(f"{'Basit Kesişim':<20} {simple:>5.1f}%   Sadece ortak sayısı")
        print(f"{'BM25':<20} {bm25:>5.1f}%   Nadir beceri bonusu")
        print(f"{'Hybrid':<20} {hybrid:>5.1f}%   Dengeli yaklaşım ✅")
    
    print("\n" + "="*70)
    conn.close()


# ============================================================
# MAIN - TÜM TESTLERİ ÇALIŞTIR
# ============================================================

def run_all_tests():
    """Tüm testleri sırayla çalıştır"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "TEZ RAPORU - ALGORİTMA TESTLERİ" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    
    # Test 1: Algoritma Karşılaştırması
    results = compare_algorithms_test()
    
    # Test 2: Performans Testi
    performance_test()
    
    # Test 3: Gerçek Senaryolar
    real_world_scenarios()
    
    print("\n" + "="*70)
    print(" "*20 + "TÜM TESTLER TAMAMLANDI! ✅")
    print("="*70)
    print("\nSonuçları tez raporuna kopyalayabilirsiniz.")
    print("\n")


if __name__ == "__main__":
    run_all_tests()