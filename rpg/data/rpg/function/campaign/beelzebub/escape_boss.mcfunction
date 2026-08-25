particle minecraft:flash{color:5925662} ~ ~1 ~ 0 0 0 0 1 force
particle minecraft:spore_blossom_air ~ ~1 ~ 2.8 1.2 2.8 0.08 90 force
particle minecraft:large_smoke ~ ~1 ~ 1.4 0.8 1.4 0.06 45 force
tellraw @a[tag=rpg.ch1.current,distance=..48] ["",{"text":"别西卜：","color":"#5A6B1E","bold":true,"italic":false},{"text":"裁决的是名字，不是饥饿。我们会再见。","color":"#B5D957","bold":false,"italic":false}]
function rpg:campaign/beelzebub/ui/escape/start
kill @s
