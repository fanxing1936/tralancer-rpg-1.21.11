bossbar set rpg:chapter1 color red
bossbar set rpg:chapter1 name ["",{"text":"尾声｜救下米拉 · 见证人","color":"#FF806B","bold":true,"italic":false}]
execute unless entity @s[tag=rpg.ch1.ui.title.9] run function rpg:campaign/beelzebub/ui/title/stage9
