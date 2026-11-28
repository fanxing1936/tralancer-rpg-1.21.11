function rpg:town/ev/title2
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#A8B4C0","bold":true,"italic":false},{"text":"守夜人","color":"#A8B4C0","bold":true,"italic":false},{"text":"〗","color":"#A8B4C0","bold":true,"italic":false},{"text":" 𝔚𝔞𝔱𝔠𝔥𝔪𝔞𝔫","color":"#8F7430","italic":false},{"text":"  它们从墓地出来了！看着它们，别让它们靠近镇口！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"They're coming out of the graveyard! Watch them; don't let them reach the gate!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ho01 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
tellraw @a[tag=rpg.tw.in] ["",{"text":"〖副本〗","color":"#C9A646","bold":true,"italic":false},{"text":"  空心人从墓地出来了。看着它们，它们就不动；一转身，它就近了一点。别让它们走到天使像。","color":"#9C9A94","bold":false,"italic":false}]
scoreboard players set #ph rpg_te 1
scoreboard players set #wave rpg_te 0
scoreboard players set #reach rpg_te 0
bossbar set rpg:town_ev max 3
bossbar set rpg:town_ev value 0
function rpg:town/ev/h/wave
