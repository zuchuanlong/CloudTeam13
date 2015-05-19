// total Festival map
function(doc){
    if(doc.text.match(/festival|valent.*day|mother.*day|mother.+fest|mum.+festival|new.*\syear|easter|earth.*day|sport.*fes|fest.*sport|ball.*fes|fest.*ball|horse.*fest|fest.*horse|AAE Arizona Cup|Fiesta de los Vaqueros|Fiesta Bowl|Oldest Rodeo|music.*fest|fest.*music|mcdowell.+mountain|viva.+phoenix|tempe music festival|film.+fest|film.*fest|fest.*film|fest.+film|screenplay|film.*day｜day.*film/i)&& doc.urban_village){
        if(doc.urban_village != 'und'){emit(doc.urban_village, 1);}
    }
}
// total Festival reduce
_count

// total Pet map
function(doc){
    if(doc.text.match(/bird|dog|puppy|cat|kitty|fish|bull/i)&& doc.urban_village){
        if(doc.urban_village != 'und'){emit(doc.urban_village, 1);}
    }
}

// total Pet reduce
_count

// total sport map
function(doc){
    if(doc.text.match(/AZCardinals|ArizonaRattlers|cardinals|rattlers|footbal|nfc|afl|cfl|ncaaf|Dbacks|LosDbacks|diamonbacks|baseball|mlb|ncaab|hoenixMercury|suns|mercury|basketball|nba|ncaab|coyotesbuzztap|ArizonaCoyotes|coyotes|hockey|nhl|AZUnitedSC|united\ssc|soccer|usl/i) && doc.urban_village){
        if(doc.urban_village != 'und'){emit(doc.urban_village, 1);}
    }
}
// total sport reduce
_count

// total tourist map
function(doc){
    if(doc.text.match(/Heard Museum|Indian Fair and Market|Indian fair & market|HeardMuseum|The Heard|phoenix zoo|phoenixzoo|\spz$|^pz$|\#pz$|\szoo$|^zoo$|\#zoo$|Arizona Science Center|ArizonaScienceCenter|azsciencecenter|AZ Science Center|ASC|Arizona Science Centre|ArizonaScienceCentre|azsciencecentre|AZ Science Centre|Camelback Mountain|CamelbackMountain|Cew S-wegiom|Echo Canyon trail|Cholla trail|skicamelback|camelback|Resort Arena|Talking Stick Resort Arena|TalkingStickResortArena|America West Arena|AmericaWestArena|US Airways Center|US AirwaysCenter|usairwayscente|USAC|airways centre|TSRA|/i)&& doc.urban_village){
        if(doc.urban_village != 'und'){emit(doc.urban_village, 1);}
    }
}
// total tourist reduce
_count

// total emoji with urban map
function(doc) {
    if (doc.text.match(/([\uE000-\uF8FF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDDFF])/) && doc.urban_village){
        if(doc.urban_village != 'und'){
            emit(doc.urban_village, 1);
        }
    }
}
// total emoji with urban reduce
_count

// urban_village map
function(doc) {
    if (doc.urban_village){
        if(doc.urban_village != "und"){
            emit(doc.urban_village,1);
        }
    }
}
// urban_village reduce
_count

// general day map
function(doc) { 
created_at = doc.created_at.split(" ");
var sentiment = doc.sentiment_score;
day = created_at[2];
    var rank = 0;
        if (sentiment > 0){
            rank = 1
        }else if (sentiment < 0){
            rank = -1
        }
emit([day,rank] , 1);}
// general reduce
_count

// general hour map
function(doc) {
var sentiment = doc.sentiment_score;
    var created_at = doc.created_at.split(" ")
    var hour_raw = Number(created_at[3].substr(0,2)) - 7
    var hour = hour_raw
    if (hour_raw < 0){
        hour = hour_raw + 24
    }
    var rank = 0;
        if (sentiment > 0){
            rank = 1
        }else if (sentiment < 0){
            rank = -1
        }
    emit([hour,rank] , 1);
}
// general hour reduce
_count

// general month map
function(doc) { 
var sentiment = doc.sentiment_score;
    created_at = doc.created_at.split(" ");
    month = created_at[1];
    if (month == 'Jan'){
    month = 1;
    }else if (month == 'Feb'){
    month = 2;
    }else if (month == 'Mar'){
    month = 3;
    }else if (month == 'Apr'){
    month = 4;
    }else if (month == 'May'){
    month = 5;
    }else if (month == 'Jun'){
    month = 6;
    }else if (month == 'Jul'){
    month = 7;
    }else if (month == 'Aug'){
    month = 8;
    }else if (month == 'Sep'){
    month = 9;
    }else if (month == 'Oct'){
    month = 10;
    }else if (month == 'Nov'){
    month = 11;
    }else if (month == 'Dec'){
    month = 12;
    }
    var rank = 0;
        if (sentiment > 0){
            rank = 1
        }else if (sentiment < 0){
            rank = -1
        }
    emit([month, rank], 1);
}
// general month reduce
_count

// general year map
function(doc) { 
var sentiment = doc.sentiment_score;
created_at = doc.created_at.split(" ");
year = created_at[5];
    var rank = 0;
        if (sentiment > 0){
            rank = 1
        }else if (sentiment < 0){
            rank = -1
        }
emit([year, rank], 1);}
// general year reduce
_count

// general language map
function(doc) {
  emit(doc.lang, 1);
}
// general language reduce
_count

