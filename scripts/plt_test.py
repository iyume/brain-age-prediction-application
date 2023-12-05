import matplotlib.pyplot as plt

# fmt: off
losses = [29.916577750894074, 14.466186557052831, 13.740846514992121, 13.384288217643753, 11.709602415781497, 11.225658654219718, 9.547018762299917, 9.380280594448111, 8.63849095533362, 8.70751353922183, 8.449958674834416, 7.844351489493188, 6.969408676224119, 6.767215843629049, 6.088025840687132, 5.923712251361099, 5.432847104354389, 5.163407778548292, 5.206392065638909, 5.118533534192023, 4.763043311177701, 4.641350221927002, 4.391632563295657, 4.087243993006137, 3.9239895627740977, 3.78191923763735, 3.8084171003201877, 3.6022167096690367, 3.6580149784719405, 3.5759068100615874, 3.658922035902668, 3.253838285982748, 3.1983477620424687, 3.493468320070994, 3.284574390303159, 2.946066807956561, 3.5504065797909496, 2.8621509289572424, 2.8175466665308533, 2.8037768177501414, 2.950788781434366, 2.755910931152092, 2.824155086805916, 2.618079744614044, 2.9810705967941473, 2.8182165934740793, 2.7806606871241946, 2.568237914182334, 2.628278453908069, 2.836296034310162, 2.6366132586503985, 2.5952636701615437, 2.5632921894109577, 2.34960913279378, 2.7620440588606177, 2.4912643570595603, 2.4656149742676576, 2.556882465691713, 2.5828681576280164, 2.3577123460927485, 2.428493981598117, 2.479938509830628, 2.4637952725656205, 2.4395686040251525, 2.42142836079248, 2.398241501778857, 2.316897098279733, 2.2308208268303127, 2.3419485986768214, 2.2485864070234003, 2.2264360334067193, 2.5356828824397235, 2.4916349792254993, 2.213178064017151, 2.130399276381689, 2.1021443769215984, 2.1078004126853123, 2.0895535016341693, 2.0726661909838375, 2.0152038695738956, 2.0481779570162444, 2.0239618956112704, 1.9275460942360818, 1.9206654537146808, 1.8916366069198498, 2.499387463644042, 2.0495427722795645, 2.2831492030592386, 2.1461847011980995, 2.082021810518089, 2.1498373909537674, 2.10256759841955, 1.9526391621853443, 2.1498261180498925, 2.5474918356460314, 1.9474397429337733, 2.036060235810336, 2.07967578274702, 1.9367454333113725, 1.983602165240204]

mae_errors = [16.62877498092651, 14.102555712890625, 11.626720278167724, 13.92029906463623, 12.76448973083496, 9.777330241394043, 10.673347428131104, 8.949360507202147, 9.623532473754882, 8.512063822555543, 7.472286689949035, 7.865388203430177, 8.963537745189665, 5.724854586029053, 5.518913655853271, 5.38491413269043, 5.236615440368652, 4.86914666442871, 6.309927465438842, 7.055660288238525, 3.6359154319763194, 3.8209914474487308, 3.3914313316345215, 5.2725119720458995, 4.941549577331543, 3.7796913208007807, 4.298984162902833, 4.318646733093262, 3.002881498718261, 4.343454506683351, 2.936581519317627, 2.895205033874512, 3.0760011116027832, 2.8220540138244634, 3.5952432907104495, 2.4953175010681155, 2.707777323913574, 2.877625247573852, 2.7765656600952147, 2.5551112808227536, 2.6380012649536138, 2.5313029708862302, 2.6856235794067382, 2.7039363357543946, 2.8200696640014646, 2.419323225402832, 3.4911769973754887, 2.1486152877807614, 3.035822499084473, 2.385328079986572, 2.6753172618865966, 2.5911883819580077, 2.967724311065674, 2.5007760982513427, 2.4125817497253417, 2.1204664039611814, 2.5682813892364496, 2.5458473930358885, 2.4534077697753904, 1.982006745910644, 2.5842933624267577, 1.7139724922180175, 1.8032980895996094, 2.424222309112549, 2.3955922355651853, 2.9471439926147456, 3.7591094718933107, 2.2642658340454105, 2.1794989578247073, 2.2778666255950926, 2.6129902751922605, 2.8497334938049317, 2.8802833419799807, 1.9660283340454108, 2.026600074768066, 2.2374748046875, 2.2967013626098636, 1.7830010086059573, 1.945798365020752, 2.0633562606811515, 2.0316839973449703, 2.0563726081848146, 2.599442483520508, 2.021073336029053, 2.3773851516723634, 2.337664678955078, 2.2807836616516104, 2.1919200027465817, 1.8409159019470216, 1.6023199386596676, 2.196539589691162, 2.175373175048828, 2.088782390594482, 2.6787305900573726, 2.503917311096191, 1.6417378982543949, 1.8514217300415041, 1.849566139984131, 1.5741094902038575, 1.9904370613098146]
# fmt: on


plt.title("Test on 100 samples")
plt.xlabel("epoch")
indexes = range(1, 101)
# plt.ylabel("MAE")
plt.plot(indexes, losses, label="losses")
plt.plot(indexes, mae_errors, label="MAE")

plt.legend()

plt.savefig("fig_output.png", dpi=100, bbox_inches="tight")
