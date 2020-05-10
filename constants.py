import re

stop_words = ['biti', 'jesam', 'budem', 'sam', 'jesi', 'budeš', 'si', 'jesmo', 'budemo', 'smo', 'jeste', 'budete',
              'ste', 'jesu', 'budu', 'su', 'bih', 'bijah', 'bjeh', 'bijaše', 'bi', 'bje', 'bješe', 'bijasmo', 'bismo',
              'bjesmo', 'bijaste', 'biste', 'bjeste', 'bijahu', 'biše', 'bjehu', 'bio', 'bili', 'budimo', 'budite',
              'bila', 'bilo', 'bile', 'ću', 'ćeš', 'će', 'ćemo', 'ćete', 'želim', 'želiš', 'želi', 'želimo', 'želite',
              'žele', 'moram', 'moraš', 'mora', 'moramo', 'morate', 'moraju', 'trebam', 'trebaš', 'treba', 'trebamo',
              'trebate', 'trebaju', 'mogu', 'možeš', 'može', 'možemo', 'možete']
transformations = {'lozi': 'loga', 'lozima': 'loga', 'pjesi': 'pjeh', 'pjesima': 'pjeh', 'vojci': 'vojka',
                   'bojci': 'bojka', 'jaci': 'jak', 'jacima': 'jak', 'čajan': 'čajni', 'ijeran': 'ijerni',
                   'laran': 'larni', 'ijesan': 'ijesni', 'anjac': 'anjca', 'ajac': 'ajca', 'ajaca': 'ajca',
                   'ljaca': 'ljca', 'ljac': 'ljca', 'ejac': 'ejca', 'ejaca': 'ejca', 'ojac': 'ojca', 'ojaca': 'ojca',
                   'ajaka': 'ajka', 'ojaka': 'ojka', 'šaca': 'šca', 'šac': 'šca', 'inzima': 'ing', 'inzi': 'ing',
                   'tvenici': 'tvenik', 'tetici': 'tetika', 'teticima': 'tetika', 'nstava': 'nstva', 'nicima': 'nik',
                   'ticima': 'tik', 'zicima': 'zik', 'snici': 'snik', 'kuse': 'kusi', 'kusan': 'kusni',
                   'kustava': 'kustva', 'dušan': 'dušni', 'antan': 'antni', 'bilan': 'bilni', 'tilan': 'tilni',
                   'avilan': 'avilni', 'silan': 'silni', 'gilan': 'gilni', 'rilan': 'rilni', 'nilan': 'nilni',
                   'alan': 'alni', 'ozan': 'ozni', 'rave': 'ravi', 'stavan': 'stavni', 'pravan': 'pravni',
                   'tivan': 'tivni', 'sivan': 'sivni', 'atan': 'atni', 'cenata': 'centa', 'denata': 'denta',
                   'genata': 'genta', 'lenata': 'lenta', 'menata': 'menta', 'jenata': 'jenta', 'venata': 'venta',
                   'tetan': 'tetni', 'pletan': 'pletni', 'šave': 'šavi', 'manata': 'manta', 'tanata': 'tanta',
                   'lanata': 'lanta', 'sanata': 'santa', 'ačak': 'ačka', 'ačaka': 'ačka', 'ušak': 'uška',
                   'atak': 'atka', 'ataka': 'atka', 'atci': 'atka', 'atcima': 'atka', 'etak': 'etka', 'etaka': 'etka',
                   'itak': 'itka', 'itaka': 'itka', 'itci': 'itka', 'otak': 'otka', 'otaka': 'otka', 'utak': 'utka',
                   'utaka': 'utka', 'utci': 'utka', 'utcima': 'utka', 'eskan': 'eskna', 'tičan': 'tični',
                   'ojsci': 'ojska', 'esama': 'esma', 'metara': 'metra', 'centar': 'centra', 'centara': 'centra',
                   'istara': 'istra', 'istar': 'istra', 'ošću': 'osti', 'daba': 'dba', 'čcima': 'čka', 'čci': 'čka',
                   'mac': 'mca', 'maca': 'mca', 'naca': 'nca', 'nac': 'nca', 'voljan': 'voljni', 'anaka': 'anki',
                   'vac': 'vca', 'vaca': 'vca', 'saca': 'sca', 'sac': 'sca', 'raca': 'rca', 'rac': 'rca',
                   'aoca': 'alca', 'alaca': 'alca', 'alac': 'alca', 'elaca': 'elca', 'elac': 'elca', 'olaca': 'olca',
                   'olac': 'olca', 'olce': 'olca', 'njac': 'njca', 'njaca': 'njca', 'ekata': 'ekta', 'ekat': 'ekta',
                   'izam': 'izma', 'izama': 'izma', 'jebe': 'jebi', 'baci': 'baci', 'ašan': 'ašni'}

word_end = ['ijima|ijega|ijemu|ijem|ijim|ijih|ijoj|ijeg|iji|ije|ija|oga|ome|omu|ima|og|om|im|ih|oj|i|e|o|a|u',
            'ima|om|o|a|u', 'ama|ima|om|a|u|e|i|', 'inom|ina|inu|ine|ima|in|om|u|i|a|e|', 'ima|ama|om|a|e|i|u|o|',
            'ovima|ova|ove|ovi|ima|om|a|e|i|u|',
            'ijima|ijega|ijemu|ijeg|ijem|ijim|ijih|ijoj|iji|ije|ija|iju|ima|ome|omu|oga|oj|om|ih|im|og|o|e|a|u|i|',
            'oga|ome|omu|ega|emu|ima|oj|ih|om|eg|em|og|uh|im|e|a', 'ima|i|e|a', 'ama|om|a|e|i|u|o', 'ama|om|a|u|e|',
            'ovima|ama|ovi|ove|ova|om|a|e|i|u|o|', 'jem|ja|ju|o|', 'ući|emo|ete|mo|em|eš|e|u|',
            'evima|evi|eva|eve|ama|ima|em|a|e|i|u|', 'ima|ama|om|a|e|i|u|o|', 'ima|ama|om|a|e|i|u|o|',
            'ima|ama|om|a|e|i|u|o|', 'ima|om|a|e|u|i|', 'ima|i|a|e', 'ima|om|a|u|e|i|', 'ama|ima|om|a|e|i|u|o|',
            'ama|om|a|e|i|u|o', 'ama|ima|om|u|a|e|i|', 'ima|om|e|a|u', 'ama|ima|om|em|a|u|i|e|',
            'ima|ama|om|em|i|e|a|u|', 'ima|om|a|e|i|u|o|', 'ima|om|a|e|i|u|o|', 'ama|ima|om|a|e|i|u|o|',
            'ima|ama|om|a|e|i|u|o|', 'ima|em|a|e|u', 'smo|ste|hu|ti|še|li|la|le|lo|t|h|o',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|ama|iji|ije|ija|iju|im|ih|oj|om|og|i|a|u|e|o|',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|iji|ije|ija|iju|im|ih|oj|om|og|i|a|u|e|o|',
            'ima|om|a|u|e|i|',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|iji|ije|ija|iju|im|ih|oj|om|og|i|a|u|e|o|',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|iji|ije|ija|iju|ega|emu|eg|em|im|ih|oj|om|og|a|e|i|o|u',
            'ama|ome|omu|oga|ima|og|om|im|ih|oj|a|u|i|o|e|', 'vši|smo|ste|še|mo|te|ti|li|la|lo|le|m|š|t|h|o',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|iji|ije|ija|iju|im|ih|oj|om|og|i|a|u|e|',
            'ijima|ijega|ijemu|ijem|ijim|ijih|ijoj|ijeg|iji|ije|ija|oga|ome|omu|ima|og|om|im|ih|oj|i|e|o|a|u|',
            'ijima|ijega|ijemu|ijem|ijim|ijih|ijoj|ijeg|iji|ije|ija|oga|ome|omu|ima|og|om|im|ih|oj|i|e|o|a|u|',
            'ijemu|ijima|ijega|ijeg|ijem|ijim|ijih|ijoj|oga|ome|omu|ima|iji|ije|ija|iju|im|ih|oj|om|og|i|a|u|e|o|',
            'jući|smo|ste|jmo|jte|ju|la|le|li|lo|mo|na|ne|ni|no|te|ti|še|hu|h|j|m|n|o|t|v|š|',
            'ujemo|ujete|ujući|ajući|ivat|ujem|uješ|ujmo|ujte|avši|asmo|aste|ati|amo|ate|aju|aše|ahu|ala|alo|ali|ale|uje|uju|uj|al|an|am|aš|at|ah|ao',
            'ismo|iste|iti|imo|ite|iše|eći|ila|ilo|ili|ile|ena|eno|eni|ene|io|im|iš|it|ih|en|i|e',
            'vši|smo|ste|smo|ste|hu|ti|mo|te|še|la|lo|li|le|ju|na|no|ni|ne|o|m|š|t|h|n',
            'uvši|usmo|uste|ući|imo|ite|emo|ete|ula|ulo|ule|uli|uto|uti|uta|em|eš|uo|ut|e|u|i',
            'vši|smo|ste|ti|mo|te|mo|te|la|lo|le|li|m|š|o',
            'jući|vši|smo|ste|jmo|jte|jem|mo|te|je|ju|ti|še|hu|la|li|le|lo|na|no|ni|ne|t|h|o|j|n|m|š',
            'ajući|asmo|aste|ajmo|ajte|amo|ate|aju|ati|aše|ahu|ala|ali|ale|alo|ana|ano|ani|ane|al|at|ah|ao|aj|an|am|aš',
            'asmo|aste|ahu|ati|emo|ete|aše|ali|ući|ala|alo|ale|mo|ao|em|eš|at|ah|te|e|u|',
            'lama|lima|lom|lu|li|la|le|lo|l', 'evima|evi|eva|eve|ama|ima|em|a|e|i|u|',
            'jući|vši|smo|ste|jmo|jte|mo|te|ju|ti|še|hu|la|li|le|lo|na|no|ni|ne|t|h|o|j|n|m|š',
            'dosmo|doste|doše|nemo|demo|nete|dete|nimo|nite|nila|vši|nem|dem|neš|deš|doh|de|ti|ne|nu|du|la|li|lo|le|t|o',
            'smo|ste|jmo|jte|vši|ti|mo|te|ju|še|la|lo|le|li|na|no|ni|ne|n|j|o|m|š|t|h',
            'asmo|aste|ati|emo|ete|ali|ala|alo|ale|aše|ahu|em|eš|at|ah|ao',
            'temo|tete|timo|tite|tući|tem|teš|tao|te|li|ti|la|lo|le',
            'vši|eći|smo|ste|še|mo|te|ti|li|la|lo|le|m|š|t|h|o',
            'jemo|jete|jem|ješ|smo|ste|jmo|jte|vši|mo|še|te|ti|ju|je|la|lo|li|le|t|m|š|h|j|o',
            'jemo|jete|jem|ješ|smo|ste|jmo|jte|vši|mo|lu|še|te|ti|ju|je|la|lo|li|le|t|m|š|h|j|o',
            'ujete|ujući|ujemo|ujem|uješ|ismo|iste|ujmo|ujte|uje|uju|iše|iti|imo|ite|ila|ilo|ili|ile|ena|eno|eni|ene|uj|io|en|im|iš|it|ih|e|i',
            'smo|ste|še|mo|te|ti|li|la|lo|le|m|š|t|h|o', 'lama|lima|lom|lu|li|la|le|lo|l',
            'lama|lima|lom|lu|li|la|le|lo|l',
            'ijega|ijemu|ijima|ijeg|ijem|ijih|ijim|ima|oga|ome|omu|iji|ije|ija|iju|oj|og|om|im|ih|a|u|i|e|o|',
            'avši|ući|emo|imo|em|eš|e|u|i',
            'ajući|alima|alom|avši|asmo|aste|ajmo|ajte|ivši|amo|ate|aju|ati|aše|ahu|ali|ala|ale|alo|ana|ano|ani|ane|am|aš|at|ah|ao|aj|an',
            'anje|enje|anja|enja|enom|enoj|enog|enim|enih|anom|anoj|anog|anim|anih|eno|ovi|ova|oga|ima|ove|enu|anu|ena|ama',
            'nijega|nijemu|nijima|nijeg|nijem|nijim|nijih|nima|niji|nije|nija|niju|noj|nom|nog|nim|nih|an|na|nu|ni|ne|no',
            'om|og|im|ih|em|oj|an|u|o|i|e|a']

word_start = ['.+(s|š)k', '.+(s|š)tv', '.+(t|m|p|r|g)anij', '.+an', '.+in', '.+on', '.+n', '.+(a|e|u)ć', '.+ugov',
              '.+ug', '.+log', '.+[^eo]g', '.+(rrar|ott|ss|ll)i', '.+uj', '.+(c|č|ć|đ|l|r)aj',
              '.+(b|c|d|l|n|m|ž|g|f|p|r|s|t|z)ij', '.+[^z]nal', '.+ijal', '.+ozil', '.+olov', '.+ol', '.+lem', '.+ram',
              '.+(a|d|e|o)r', '.+(e|i)s', '.+(t|n|j|k|j|t|b|g|v)aš', '.+(e|i)š', '.+ikat', '.+lat', '.+et',
              '.+(e|i|k|o)st', '.+išt', '.+ova', '.+(a|e|i)v', '.+[^dkml]ov', '.+(m|l)ov', '.+el', '.+(a|e|š)nj',
              '.+čin', '.+roši', '.+oš', '.+(e|o)vit', '.+ast', '.+k', '.+(e|a|i|u)va', '.+ir', '.+ač', '.+ača', '.+n',
              '.+ni', '.+((a|r|i|p|e|u)st|[^o]g|ik|uc|oj|aj|lj|ak|ck|čk|šk|uk|nj|im|ar|at|et|št|it|ot|ut|zn|zv)a',
              '.+ur', '.+(a|i|o)staj', '.+(b|c|č|ć|d|e|f|g|j|k|n|r|t|u|v)a', '.+(t|č|j|ž|š)aj',
              '.+([^o]m|ič|nč|uč|b|c|ć|d|đ|h|j|k|l|n|p|r|s|š|v|z|ž)a', '.+(a|i|o)sta', '.+ta', '.+inj', '.+as',
              '.+(elj|ulj|tit|ac|ič|od|oj|et|av|ov)i', '.+(tit|jeb|ar|ed|uš|ič)i', '.+(b|č|d|l|m|p|r|s|š|ž)i', '.+luč',
              '.+jeti', '.+e', '.+i', '.+at', '.+et', '.+', '.+', '.+', '.+']

word_patterns = [re.compile("^(%s)(%s)$" % (ws, we)) for ws, we in zip(word_start, word_end)]

if __name__ == '__main__':
    for wp in word_patterns:
        print(wp)