tellraw @a[tag=rpg.tw.in] ["",{"text":"〖","color":"#D596F2","bold":true,"italic":false},{"text":"兜帽人","color":"#D596F2","bold":true,"italic":false},{"text":"〗","color":"#D596F2","bold":true,"italic":false},{"text":" ℌ𝔬𝔬𝔡𝔢𝔡 𝔐𝔞𝔫","color":"#8F7430","italic":false},{"text":"  她走不快。挡住后面的人！","color":"#9C9A94","italic":false,"hover_event":{"action":"show_text","value":{"text":"She can't move fast. Hold off the ones behind us!","color":"#8F7430","italic":false}}}]
playsound rpg:vo.town.ew09 voice @a[tag=rpg.tw.in] ~ ~ ~ 1 1
scoreboard players add #sid rpg_say 1
execute store result score #due rpg_say run time query gametime
scoreboard players add #due rpg_say 79
function rpg:town/say/push {f:11}
