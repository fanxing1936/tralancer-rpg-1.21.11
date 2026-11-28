bossbar set rpg:prologue_zh_i2 name [{"translate":"rpg.prologue.who.beelzebub.zh","fallback":"别西卜","color":"#B5D957","italic":false,"bold":true},{"text":"：","color":"#B5D957","bold":true},{"translate":"rpg.prologue.E01.zh","fallback":"这一仗，吃不下了。","color":"#FFFFFF","italic":false}]
bossbar set rpg:prologue_en_i2 name [{"translate":"rpg.prologue.who.beelzebub.en","fallback":"Beelzebub","color":"#B5D957","italic":false,"bold":true},{"text":": ","color":"#B5D957","bold":true},{"translate":"rpg.prologue.E01.en","fallback":"This fight is more than I can swallow.","color":"#D8D2C4","italic":false}]
scoreboard players set #sub rpg_pr_i2 54
scoreboard players set #subn rpg_pr_i2 601
execute as @a[tag=rpg.pri2] at @s run playsound rpg:vo.prologue.e01 voice @s ~ ~ ~ 1 1
