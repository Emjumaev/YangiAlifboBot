from converter import to_new, to_old


def test_basic_words():
    assert to_new("O‘zbekiston") == "Özbekiston"
    assert to_new("G‘ijduvon") == "Ğijduvon"
    assert to_new("shahar") == "şahar"
    assert to_new("Chirchiq") == "Çirçiq"
    assert to_new("o‘g‘il") == "öğil"


def test_apostrophe_variants():
    for a in ["‘", "’", "'", "`", "ʻ", "ʼ"]:
        assert to_new(f"o{a}zbek") == "özbek"
        assert to_new(f"G{a}ulom") == "Ğulom"


def test_uppercase():
    assert to_new("SHAHAR") == "ŞAHAR"
    assert to_new("O‘ZBEKISTON RESPUBLIKASI") == "ÖZBEKISTON RESPUBLIKASI"
    assert to_new("CHOY") == "ÇOY"
    assert to_new("Sh Ch") == "Ş Ç"


def test_s_h_separator():
    assert to_new("Is'hoq") == "Ishoq"
    assert to_new("as’hob") == "ashob"


def test_tutuq_belgisi_kept():
    assert to_new("ma’no") == "ma’no"
    assert to_new("e'lon") == "e'lon"


def test_untouched_letters():
    assert to_new("ng, ya, yo, yu, ts") == "ng, ya, yo, yu, ts"


def test_sentence():
    src = "O‘zbekiston Respublikasi Oliy Majlisi Senati yangi alifboni ma’qulladi. Choy ichamizmi, G‘ulom?"
    assert to_new(src) == "Özbekiston Respublikasi Oliy Majlisi Senati yangi alifboni ma’qulladi. Çoy içamizmi, Ğulom?"


def test_reverse():
    assert to_old("Özbekiston") == "O‘zbekiston"
    assert to_old("şahar") == "shahar"
    assert to_old("ŞAHAR") == "SHAHAR"
    assert to_old("Çoy") == "Choy"
    assert to_old("Ishoq") == "Isʼhoq"


def test_empty():
    assert to_new("") == ""
    assert to_old("") == ""
