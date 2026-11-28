bossbar set rpg:prologue_zh_i3 name [{"translate":"rpg.prologue.who.lucifer.zh","fallback":"路西法","color":"#F2E6B8","italic":false,"bold":true},{"text":"：","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D01.zh","fallback":"他要我们跪一个还没来的人。我不跪。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i3 name [{"translate":"rpg.prologue.who.lucifer.en","fallback":"Lucifer","color":"#F2E6B8","italic":false,"bold":true},{"text":": ","color":"#F2E6B8","bold":true},{"translate":"rpg.prologue.D01.en","fallback":"He would have us kneel to one who has not yet come. I will not kneel.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i3 109
scoreboard players set #subn rpg_pr_i3 301
execute as @a[tag=rpg.pri3] at @s run playsound rpg:vo.prologue.d01 voice @s ~ ~ ~ 1 1
