import folium
import numpy as np
from pyproj import Transformer
from folium.plugins import AntPath
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView


wellrig_image_base64 = 'iVBORw0KGgoAAAANSUhEUgAAATsAAAFGCAMAAAAivsjqAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAHjUExURYODg0VFRTo6OjMzMzQ0NDk5OTExMT8/P4CAgG5ubi8vLy4uLjIyMjw8PIyMjG9vby0tLTAwMIeHh21tbTY2NoiIiGZmZiwsLImJiXNzc4aGhmdnZzc3Nzg4OCgoKIGBgWtra4qKinh4eCsrK3d3d3V1dVpaWkpKSklJSUtLS0xMTEFBQVdXVyYmJjs7O2BgYE9PTz09PUBAQENDQ0dHR1BQUHt7e6enp6+vr2lpaSoqKicnJ6ysrFFRUSEhISkpKSUlJU5OTo6OjkJCQiQkJCMjI0hISJeXlzU1NaKiomhoaHJycllZWURERFNTU7KysrCwsGNjYz4+PnZ2dnFxcZGRkXBwcIuLi6SkpE1NTVtbW2xsbKamppKSknl5eYWFhZ2dnZ+fn2VlZVZWVkZGRrGxsX5+fpSUlKqqqo2NjaioqHx8fKGhoZaWlnp6epOTkyIiIpWVlR8fH2pqal9fXxwcHHR0dKOjo39/f2JiYpqaml1dXVJSUq2trSAgIKmpqaurq5CQkFVVVbOzsxsbG4SEhKCgoKWlpR0dHV5eXn19fZ6enmRkZIKCgmFhYVhYWI+Pj7S0tJubm1RUVJmZmZycnJiYmK6urh4eHhoaGlxcXBUVFRQUFLu7uxkZGRYWFgAAAA7W3ycAAAChdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AsaCChgAAAAlwSFlzAAAOwwAADsMBx2+oZAAAJ1hJREFUeF7tnfubHLWV93FJpQFJDVKsRCFWNQ7i4gtdpme4xNUw1TBjo3gxSQYHYkgCSwyEQBKvAW8IrEngZYGEkGyuhHf33f5TX9WMplTT3TXTXe6q9g/1eYAHq9U1ru/ociSdc3TTqKUqrXbVabWrzo2n3U2HAgDDEtDKza7aDcCNp90tmNAQldG51VW7Abjx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'


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map")
        self.setGeometry(0, 0, 1670, 1000)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)


        m = folium.Map([61.678656, 76.629576],
                       tiles='OpenStreetMap',
                       zoom_start=10
        )


        transformer = Transformer.from_crs("epsg:28413", "epsg:4326", always_xy=True)
        image = f'data:image/png;base64,{wellrig_image_base64}'
        AntPath.default_js = [('antpath', 'https://cdn.jsdelivr.net/npm/leaflet-ant-path@1.3.0/dist/leaflet-ant-path.js')]


        m.get_root().header.add_child(folium.Element('''
        <style>
            .leaflet-popup-content-wrapper {
                background: transparent !important;
                box-shadow: none !important;
                padding: 0 !important;
            }
            .leaflet-popup-content {
                margin: 0 !important;
                width: 250px !important;
            }
            .leaflet-popup-tip-container {
                display: none !important;
            }
            .leaflet-popup-close-button {
                display: none !important;
            }
            .popup-box {
                width: 250px;
                box-sizing: border-box;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
                position: relative;
                overflow: visible;
            }
            .popup-header {
                background-color: #fac503;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 15px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
            .popup-content {
                padding: 15px;
            }
            .popup-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
                font-size: 14px;
            }
            .popup-row:last-child {
                margin-bottom: 0;
            }
            .popup-box::after {
                content: "";
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 10px 10px 0 10px;
                border-style: solid;
                border-color: #ffffff transparent transparent transparent; 
            }
            .label {
                font-weight: bold;
            }
            .leaflet-tooltip {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                opacity: 1 !important
            }
            .leaflet-tooltip-top:before {
                display: none !important;
            }
            .custom-tooltip {
                background-color: #fac503;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 8px;
                position: relative;
                margin-bottom: 10px; 
            }
            .custom-tooltip::after {
                content: "";
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 8px 8px 0 8px;
                border-style: solid;
                border-color: #ffffff transparent transparent transparent;
            }
            .custom-trajectory {
                background-color: #fac503;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border-radius: 8px;
                position: relative;
                margin-bottom: 10px; 
            }
        </style>
        '''))


        html1_wellhead_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Well: SIBWELL17(head)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Status</span>
                    Drilling
                </div>
                <div class="popup-row">
                    <span class="label">Start date</span>
                    17.01.2023
                </div>
                <div class="popup-row">
                    <span class="label">Drilling meterage</span>
                    {drilled1}
                </div>
            </div>
        </div>
        '''

        html1_wellhead_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL17(head)
        </div>
        '''

        html1_wellbottom_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Well: SIBWELL17(bottom)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Total depth</span>
                    {tvdss1}
                </div>
            </div>
        </div>
        '''

        html1_wellbottom_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL17(bottom)
        </div>
        '''

        html1_trajectory = '''
        <div class="custom-trajectory">
            Wellbore trajectory to the bottom of SIBWELL17
        </div>
        '''

        x1_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.052359399, 0.209431854, 0.471200141, 0.837635554, 1.308697909, 1.884335548, 2.564485347, 3.349072719, 4.238011626, 5.231204585, 6.328542682, 7.529905581, 8.835161539, 10.24416742, 11.75676871, 13.37279954, 15.09208269, 16.91442961, 18.83964048, 20.86750417, 22.94662116, 25.02573833, 27.10485566, 29.18397317, 31.26309084, 33.34220869, 35.42132671, 37.5004449, 39.57956326, 41.65868179, 43.73780049, 45.81691936, 47.8960384, 49.97515761, 52.054277, 54.13339655, 56.21251628, 58.29163617, 60.37075624, 62.44987648, 64.52899689, 66.60811746, 68.68723821, 70.76635913, 72.84548022, 74.92460149, 77.00372292, 79.08284452, 81.16196629, 83.24108824, 85.32021035, 87.39933264, 89.4784551, 91.55757772, 93.63670052, 95.71582349, 97.79494663, 99.87406994, 101.9531934, 104.0323171, 106.1114409, 108.1905649, 110.2696891, 112.3488134, 114.4279379, 116.5070626, 118.5861874, 120.6653124, 122.7444376, 124.823563, 126.9026885, 127.4561518, 128.9818143, 131.0609404, 133.1400666, 135.219193, 137.2983195, 139.3774462, 141.4565731, 143.5357002, 145.6148274, 147.6939549, 149.7730824, 151.8522102, 153.9313381, 156.0104662, 158.0895945, 160.1687229, 162.2478515, 164.3269803, 166.4061092, 168.4852383, 170.5643676, 172.6434971, 174.7226267, 176.8017565, 178.8808865, 180.9600166, 183.0391469, 185.1182774, 187.197408, 189.2765389, 191.3556698, 193.434801, 195.5139323, 197.5930638, 199.6721955, 201.7513274, 203.8304594, 205.9095916, 207.9887239, 210.0678565, 212.1469892, 214.226122, 216.3052551, 218.3843883, 220.4635217, 222.5426552, 224.6217889, 226.7009228, 228.7800569, 230.8591911, 232.9383255, 235.0174601, 237.0965949, 239.1757298, 241.2548649, 243.3340001, 244.3735679, 245.4004155, 247.3778664, 249.2534919, 251.026959, 252.6980294, 254.2664993, 255.7321294, 257.0947183, 258.3541519, 259.5102651, 260.5628489, 261.5117841, 262.3570086, 263.0983615, 263.7357204, 264.2690476, 264.6982593, 265.0232816, 265.2440826, 265.360648, 265.3729632, 265.2810178, 265.0848216, 264.7843945, 264.3797939, 263.871072, 263.258267, 262.5414941, 261.7208155, 260.7966489, 259.768248, 258.7896981, 258.6366213, 257.4016213, 256.5782474, 256.063361, 254.6220903, 253.0779823, 251.4311649, 249.6818991, 247.8304324, 246.0739137, 245.877472, 245.3814815, 243.8831392, 241.8888063, 239.8944733, 237.9001401, 235.9058068, 233.9114734, 231.9171399, 229.9228062, 227.9284725, 225.9341385, 223.9398045, 221.9454704, 219.9511361, 217.9568017, 217.3465353, 215.9229325, 213.7327728, 211.3792451, 208.863114, 206.1850909, 203.345998, 200.3467131, 197.1881928, 193.8713655, 190.3972502, 186.7669107, 182.9814205, 179.0419257, 174.9496456, 170.7058735, 166.3118487, 161.768897, 157.0784392, 152.2419145, 147.2607928, 142.1365666, 136.8707445, 131.4650152, 125.9210278, 120.240412, 114.4249363, 108.4763413, 103.1083787, 102.3964376, 96.18712849, 89.85029645, 87.83130355, 83.38783004, 80.1100853, 76.80170074, 70.09398519, 63.26664431, 56.32179582, 49.26155852, 42.08807893, 34.80350697, 27.41006695, 19.9100563, 12.30571846, 10.15966783, 4.625560945, 3.078746547, -3.058564308, -10.74268967, -18.42681513, -26.11094068, -33.79506633, -41.23944734, -41.47919207, -49.16331799, -56.847444, -64.35560362, -64.53157011, -70.76185971, -72.21735606, -79.964888, -87.80259348, -95.72808507, -103.7389486, -111.8327438, -120.0070053, -128.2592432, -136.5869436, -144.98757, -153.4585633, -161.9973434, -167.6981108, -170.6013282, -179.2678587, -187.9943141, -196.7780362, -205.6163494, -214.5065616, -223.4459646, -232.4318354, -241.4614369, -250.5320185, -259.6408172, -268.7850585, -277.9619568, -287.1687169, -296.4025343, -304.1138683, -305.6606063, -314.9400926, -324.2381767, -329.2984812, -329.7455933, -333.5507988, -334.2783057, -342.873771, -352.2115915, -361.5583273, -363.6787878, -364.731572, -370.9080761, -380.2579157, -389.6077554, -398.957595, -408.3074347, -417.6572743, -427.007114, -436.3569536, -445.7067932, -455.0566329, -464.4064726, -473.7563122, -483.1061519, -492.4559915, -501.8058312, -511.1556708, -520.5055105, -529.8553501, -539.2051898, -548.5550295, -557.9048691, -567.2547088, -576.6045485, -585.9543881, -595.3042278, -604.6540675, -614.0039071, -623.3537468, -632.7035865, -642.0534261, -651.4032658, -660.7531055, -670.1029452, -679.4527848, -688.8026245, -698.1524642, -707.5023039, -716.8521436, -726.2019832, -735.5518229, -744.9016626, -754.2515023, -763.601342, -772.9511817, -782.3010214, -791.650861, -801.0007007, -810.3505404, -816.3737072, -819.7002999, -829.0481268, -831.1685669, -838.3929161, -847.7375666, -857.082217, -865.4924024, -866.4268674, -875.7715179, -885.1161683, -894.4608188, -903.8054692, -913.1501197, -922.4947702, -931.8394206, -941.1840711, -950.5287216, -959.8733721, -969.2180226, -978.5626731, -980.6773675, -987.9087355, -990.7544064, -997.257472, -1006.60633, -1015.955188, -1025.304046, -1034.652904, -1044.001762, -1053.35062, -1062.699478, -1072.048336, -1077.666064, -1081.396974, -1090.742402, -1092.858351, -1100.08373, -1109.424879, -1118.766027, -1128.107176, -1137.448325, -1146.789474, -1156.130623, -1165.471772, -1174.812921, -1184.154069, -1193.495218, -1202.836367, -1212.177516, -1221.518665, -1230.859814, -1240.200963, -1249.542112, -1258.883261, -1268.22441, -1277.565559, -1286.906708, -1296.247857, -1305.518013, -1450]
        y1_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.005979573, -0.05397742, -0.149945825, -0.29386941, -0.485742573, -0.725548939, -1.013242932, -1.348774906, -1.73212525, -2.163250603, -2.6420665, -3.168514222, -3.742560237, -4.364099189, -5.033038751, -5.749323947, -6.512841639, -7.323461512, -8.181092577, -9.085695537, -10.03707782, -11.03506547, -12.07962472, -13.17062752, -14.30787365, -15.49122561, -16.72057671, -17.99569018, -19.31644524, -20.68225914, -22.09416675, -23.35870133, -23.55074688, -25.05222979, -26.01230713, -26.5984667, -28.18918085, -29.82417639, -31.50330735, -33.22633201, -34.99298327, -36.62284685, -36.80285256, -37.25734415, -38.63032184, -40.45779126, -42.28526079, -44.11273044, -45.9402002, -47.76767007, -49.59514006, -51.42261016, -53.25008038, -55.07755071, -56.90502115, -58.7324917, -60.55996237, -62.38743315, -62.94663925, -64.22467076, -66.10042557, -68.01608816, -69.97101904, -71.96465806, -73.9964055, -76.06563536, -78.17168977, -80.31397328, -82.49181216, -84.7045059, -86.95140376, -89.23183724, -91.54511296, -93.89050184, -96.26731515, -98.67483142, -101.112311, -103.5790047, -106.0741738, -108.597066, -111.1468979, -113.7228674, -116.324187, -118.9501183, -121.5998212, -124.2724809, -126.653637, -126.9673507, -129.6835172, -132.4202375, -133.285053, -135.1766424, -136.5619399, -137.9518582, -140.7451142, -143.5555306, -146.3822008, -149.2242931, -152.0809621, -154.9512829, -157.834436, -160.7295594, -163.6357182, -164.4507102, -166.5494946, -167.1361168, -169.4636635, -172.3778324, -175.2920014, -178.2061705, -181.1203395, -183.9435865, -184.0345086, -186.9486778, -189.862847, -192.7102817, -192.7770162, -195.1398247, -195.6918149, -198.6300305, -201.6024441, -204.60815, -207.6462329, -210.7157673, -213.8158181, -216.9454411, -220.1036829, -223.2895815, -226.5021665, -229.7404593, -231.902449, -233.0034807, -236.2902222, -239.59969, -242.930876, -246.2827653, -249.6543371, -253.0445643, -256.4524142, -259.8768487, -263.3168248, -266.7712945, -270.2392057, -273.7195019, -277.211123, -280.7130054, -283.6374932, -284.2240864, -287.7432886, -291.2695439, -293.188641, -293.3581035, -294.7994632, -295.0750328, -298.331478, -301.8705669, -305.414527, -306.2187442, -306.6180498, -308.960707, -312.5069636, -316.0532203, -319.599477, -323.1457337, -326.6919904, -330.2382471, -333.7845038, -337.3307605, -340.8770172, -344.4232739, -347.9695306, -351.5157873, -355.062044, -358.6083007, -362.1545574, -365.7008141, -369.2470708, -372.7933276, -376.3395843, -379.885841, -383.4320977, -386.9783544, -390.5246111, -394.0708678, -397.6171245, -401.1633812, -404.7096379, -408.2558946, -411.8021513, -415.348408, -418.8946647, -422.4409214, -425.9871782, -429.5334349, -433.0796916, -436.6259483, -440.172205, -443.7184617, -447.2647184, -450.8109751, -454.3572318, -457.9034886, -461.4497453, -464.996002, -468.5422587, -472.0885154, -475.6347721, -477.9192707, -479.1809652, -482.7261786, -483.5303457, -486.2701467, -489.8140621, -493.3579775, -496.5475013, -496.9018929, -500.4458083, -503.9897237, -507.5336391, -511.0775545, -514.6214699, -518.1653853, -521.7093007, -525.2532161, -528.7971315, -532.341047, -535.8849624, -539.4288778, -540.2308659, -542.9734731, -544.0528226, -546.5194696, -550.0655406, -553.6116116, -557.1576826, -560.7037536, -564.2498246, -567.7958956, -571.3419666, -574.8880376, -577.0188717, -578.4339879, -581.978385, -582.7808489, -585.5210402, -589.0636277, -592.6062151, -596.1488025, -599.69139, -603.2339774, -606.7765649, -610.3191523, -613.8617398, -617.4043272, -620.9469147, -624.4895021, -628.0320896, -631.574677, -635.1172645, -638.659852, -642.2024395, -645.7450269, -649.2876144, -652.8302019, -656.3727894, -659.9153769, -663.4310407, -700]
        z1_list = [0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 159.9998172, 169.9985379, 179.9950654, 189.9883037, 199.9771568, 209.9605294, 219.9373266, 229.9064544, 239.8668195, 249.8173297, 259.7568939, 269.6844219, 279.5988252, 289.4990166, 299.3839103, 309.2524224, 319.1034706, 328.9359748, 338.7488566, 348.5410399, 358.3225159, 368.1039919, 377.8854678, 387.6669437, 397.4484195, 407.2298953, 417.0113711, 426.7928468, 436.5743225, 446.3557982, 456.1372738, 465.9187494, 475.700225, 485.4817005, 495.2631759, 505.0446514, 514.8261268, 524.6076022, 534.3890775, 544.1705528, 553.9520281, 563.7335033, 573.5149785, 583.2964536, 593.0779288, 602.8594038, 612.6408789, 622.4223539, 632.2038289, 641.9853038, 651.7667787, 661.5482536, 671.3297284, 681.1112032, 690.892678, 700.6741527, 710.4556274, 720.237102, 730.0185766, 739.8000512, 749.5815257, 759.3630002, 769.1444747, 778.9259491, 788.7074235, 798.4888979, 808.2703722, 818.0518465, 827.8333207, 837.6147949, 847.3962691, 850.0000975, 857.1777432, 866.9592173, 876.7406913, 886.5221653, 896.3036393, 906.0851132, 915.8665871, 925.6480609, 935.4295347, 945.2110085, 954.9924822, 964.7739559, 974.5554296, 984.3369032, 994.1183768, 1003.89985, 1013.681324, 1023.462797, 1033.244271, 1043.025744, 1052.807218, 1062.588691, 1072.370164, 1082.151638, 1091.933111, 1101.714584, 1111.496057, 1121.27753, 1131.059003, 1140.840476, 1150.621949, 1160.403422, 1170.184895, 1179.966368, 1189.747841, 1199.529314, 1209.310787, 1219.092259, 1228.873732, 1238.655205, 1248.436678, 1258.21815, 1267.999623, 1277.781095, 1287.562568, 1297.34404, 1307.125513, 1316.906985, 1326.688457, 1336.46993, 1346.251402, 1356.032874, 1365.814347, 1375.595819, 1385.377291, 1395.158763, 1400.049499, 1404.942911, 1414.745273, 1424.567275, 1434.407652, 1444.265117, 1454.138379, 1464.026153, 1473.927147, 1483.840056, 1493.763586, 1503.696446, 1513.637336, 1523.584948, 1533.537987, 1543.495156, 1553.455146, 1563.416658, 1573.378393, 1583.339047, 1593.297311, 1603.251889, 1613.201486, 1623.144791, 1633.080503, 1643.007329, 1652.923971, 1662.829125, 1672.721508, 1682.599818, 1692.459807, 1702.309062, 1710.859815, 1712.137424, 1721.946565, 1728.06009, 1731.735187, 1741.502033, 1751.245822, 1760.965257, 1770.659078, 1780.326028, 1789.016695, 1789.964975, 1792.359259, 1799.592175, 1809.219376, 1818.846576, 1828.473777, 1838.100977, 1847.728178, 1857.355378, 1866.982579, 1876.609779, 1886.236979, 1895.864179, 1905.491379, 1915.11858, 1924.74578, 1927.691703, 1934.36276, 1943.937842, 1953.466148, 1962.944797, 1972.370881, 1981.741527, 1991.053887, 2000.305144, 2009.492457, 2018.613039, 2027.664121, 2036.642928, 2045.546717, 2054.372784, 2063.118469, 2071.781077, 2080.357959, 2088.846526, 2097.244199, 2105.548416, 2113.75663, 2121.866312, 2129.875053, 2137.780418, 2145.579941, 2153.271285, 2160.852088, 2167.459593, 2168.320013, 2175.672862, 2182.908356, 2185.159303, 2190.024269, 2193.536702, 2197.018449, 2203.888801, 2210.633164, 2217.249543, 2223.735915, 2230.090291, 2236.31072, 2242.395285, 2248.34218, 2254.149568, 2255.749269, 2259.852629, 2260.999542, 2265.550158, 2271.247687, 2276.945216, 2282.642745, 2288.340274, 2293.860039, 2294.037802, 2299.73533, 2305.432858, 2310.999913, 2311.130386, 2315.749941, 2316.825347, 2322.42357, 2327.87633, 2333.181966, 2338.338863, 2343.345448, 2348.200198, 2352.901633, 2357.448322, 2361.838878, 2366.071966, 2370.146295, 2372.760968, 2374.060576, 2377.813714, 2381.404516, 2384.831889, 2388.094789, 2391.192223, 2394.123246, 2396.886965, 2399.48254, 2401.909178, 2404.166142, 2406.252744, 2408.168347, 2409.912369, 2411.484278, 2412.662003, 2412.883518, 2414.109818, 2415.162726, 2415.662114, 2415.704224, 2416.064942, 2416.133907, 2416.840763, 2417.364805, 2417.635989, 2417.662292, 2417.671008, 2417.715627, 2417.783171, 2417.850714, 2417.918257, 2417.9858, 2418.053343, 2418.120885, 2418.188428, 2418.25597, 2418.323512, 2418.391054, 2418.458596, 2418.526137, 2418.593679, 2418.66122, 2418.728761, 2418.796302, 2418.863842, 2418.931383, 2418.998923, 2419.066463, 2419.134003, 2419.201543, 2419.269083, 2419.336622, 2419.404161, 2419.4717, 2419.539239, 2419.606778, 2419.674317, 2419.741855, 2419.809393, 2419.876931, 2419.944469, 2420.012007, 2420.079545, 2420.147082, 2420.214619, 2420.282156, 2420.349693, 2420.41723, 2420.484766, 2420.552302, 2420.619839, 2420.687375, 2420.75491, 2420.822446, 2420.889981, 2420.933488, 2420.968571, 2421.185496, 2421.259003, 2421.524766, 2421.868528, 2422.212289, 2422.521675, 2422.556051, 2422.899812, 2423.243573, 2423.587334, 2423.931094, 2424.274855, 2424.618615, 2424.962375, 2425.306135, 2425.649895, 2425.993654, 2426.337414, 2426.681173, 2426.758966, 2426.972698, 2427.02816, 2427.136449, 2427.292126, 2427.447803, 2427.603479, 2427.759155, 2427.914832, 2428.070507, 2428.226183, 2428.381859, 2428.475404, 2428.551429, 2428.863962, 2428.958988, 2429.298812, 2429.738144, 2430.177476, 2430.616808, 2431.05614, 2431.495471, 2431.934802, 2432.374134, 2432.813465, 2433.252795, 2433.692126, 2434.131456, 2434.570787, 2435.010117, 2435.449447, 2435.888777, 2436.328106, 2436.767436, 2437.206765, 2437.646094, 2438.085423, 2438.524751, 2438.960741, 2800]
        y1_northing = [6842313.838 + y1 for y1 in y1_list]
        x1_easting = [13586273.084 - x1 for x1 in x1_list]
        WELL_LAT17 = 61.678656
        WELL_LON17 = 76.629576
        raw_coordinates1 = []
        coordinates1 = []

        ok1 = ~(np.isnan(x1_list) | np.isnan(y1_list) | np.isnan(z1_list))
        dEW1, dNS1, tvd1 = np.array(x1_list)[ok1], np.array(y1_list)[ok1], np.array(z1_list)[ok1]
        tvdss1 = tvd1[-1]
        drilled1 = np.sum(np.sqrt(np.diff(dEW1)**2 + np.diff(dNS1)**2 + np.diff(tvd1)**2))

        tooltip1_head = folium.Tooltip(html1_wellhead_small, sticky=False, direction='top')
        folium.Marker(location=[61.678656, 76.629576],
            tooltip=tooltip1_head,
            popup=html1_wellhead_full.format(drilled1=f'{drilled1:.0f}m.'),
            icon=folium.CustomIcon(image, icon_size=(44, 46), icon_anchor=(22, 46))
        ).add_to(m)

        for x, y in zip(x1_easting, y1_northing):
            if np.isnan(x) or np.isnan(y):
                continue
            lon, lat = transformer.transform(x, y)
            raw_coordinates1.append((lat, lon))

        delta_lat = WELL_LAT17 - raw_coordinates1[0][0]
        delta_lon = WELL_LON17 - raw_coordinates1[0][1]
        for lat, lon in raw_coordinates1:
            coordinates1.append((lat + delta_lat, lon + delta_lon))

        AntPath(
            locations=coordinates1,
            delay=1200,
            dash_array=[10, 50],
            color='#FFFF00',
            pulse_color='#000000',
            weight=6,
            opacity=0.5,
            tooltip=html1_trajectory
        ).add_to(m)

        tooltip1_bottom = folium.Tooltip(html1_wellbottom_small, sticky=False, direction='top')
        last_lat1, last_lon1 = coordinates1[-1]
        folium.CircleMarker(
            location=[last_lat1, last_lon1],
            radius=8,
            color="#FFFF00",
            opacity=1.0,
            fill=True,
            fill_color="#000000",
            fill_opacity=0.8,
            tooltip=tooltip1_bottom,
            popup=html1_wellbottom_full.format(tvdss1=f'{tvdss1:.0f}m.'),
        ).add_to(m)


        html2_wellhead_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Well: SIBWELL18(head)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Status</span>
                    Digging
                </div>
                <div class="popup-row">
                    <span class="label">Start date</span>
                    17.01.2023
                </div>
                <div class="popup-row">
                    <span class="label">Drilling meterage</span>
                    {drilled2}
                </div>
            </div>
        </div>
        '''

        html2_wellhead_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL18(head)
        </div>
        '''

        html2_wellbottom_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Скважина: SIBWELL18(bottom)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Depth</span>
                    {tvdss2}
                </div>
            </div>
        </div>
        '''

        html2_wellbottom_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL18(bottom)
        </div>
        '''

        html2_trajectory = '''
        <div class="custom-trajectory">
            Wellbore trajectory to the bottom of SIBWELL18
        </div>
        '''

        x2_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.048512693, -0.194017306, -0.436493476, -0.775893931, -1.212152505, -1.745184148, -2.374884945, -3.101132135, -3.923784133, -4.842680563, -5.857642283, -6.195936769, -6.945929359, -8.038935708, -9.131943255, -10.224952, -11.31796194, -12.41097308, -13.50398542, -14.59699895, -15.69001368, -16.78302961, -17.87604674, -18.96906506, -20.06208458, -21.1551053, -22.24812722, -23.34115034, -24.43417465, -25.52720016, -26.62022686, -27.71325477, -28.80628387, -29.89931417, -30.99233323, -32.0853403, -33.17834744, -34.27135402, -35.36436039, -36.45736677, -37.55037315, -38.64337953, -39.73638561, -40.82939202, -41.92239855, -43.01540519, -44.10841196, -45.20141885, -46.29442586, -47.38743298, -48.48044023, -49.5734476, -50.66645509, -51.75946269, -52.85247042, -53.94547826, -55.03848623, -56.13149432, -57.22450252, -58.31751085, -59.41051929, -60.50352785, -61.59653654, -62.12548685, -62.71260746, -63.78669764, -63.97964967, -65.30987208, -66.64009462, -67.9703173, -69.30054011, -70.63076305, -71.96098612, -73.29120932, -74.62143266, -75.95165612, -77.08892751, -77.28187974, -78.6121036, -79.9423276, -81.27255172, -81.74471116, -82.62098482, -84.05124512, -85.56841979, -87.17204666, -88.86163728, -89.48192844, -90.61998999, -92.38810203, -94.16038217, -95.93629056, -97.71528623, -98.34737649, -99.47040867, -101.1085587, -102.6212381, -104.007986, -105.26838, -106.4020362, -107.4086093, -108.2877926, -109.0393184, -109.6629578, -110.1585207, -110.5258561, -110.7648524, -110.8153267, -110.9044054, -111.0370348, -111.1696644, -111.302294, -111.3800358, -111.4268109, -111.4728567, -111.4241449, -111.2806903, -111.0425367, -110.7097565, -110.2824513, -109.760751, -109.1448147, -108.43483, -107.6310131, -106.7336088, -105.7428906, -104.6591602, -103.4827477, -102.2140115, -100.8533381, -99.40114186, -97.85786521, -96.22397823, -94.49997862, -92.68639153, -90.78376939, -88.79269176, -86.71376514, -84.54762279, -82.29492454, -79.95635659, -77.53263128, -75.0244869, -72.43268746, -69.75802245, -67.0013066, -64.16337962, -63.57165203, -61.24510598, -58.24737461, -55.17109866, -52.01721518, -48.78668487, -45.48049179, -42.09964304, -38.64516846, -35.11812031, -31.51957296, -27.85062257, -25.79719509, -24.11927293, -21.72140848, -20.3774467, -16.6356204, -12.89379406, -9.151967667, -5.410141231, -1.668314748, 2.073511781, 5.815338355, 8.205498194, 9.557164992, 11.62106913, 13.30455592, 17.09846898, 20.94621563, 24.84661309, 28.79846237, 32.80054871, 36.85164187, 40.95049657, 45.09585283, 49.28643639, 53.52095908, 57.79811922, 62.11660202, 64.69687503, 65.25158387, 66.47337636, 70.86562365, 75.29528908, 79.76101098, 84.26141662, 88.79512257, 93.22240237, 93.36073521, 97.95685107, 102.5820573, 107.2349322, 111.9140455, 116.6179587, 121.345226, 126.0943942, 129.4553574, 130.8631657, 133.1858481, 135.6368474, 136.6158799, 136.9500376, 140.4136507, 145.2010926, 149.9980425, 154.8028968, 157.5479344, 157.9328627, 159.6139222, 164.4297717, 168.3759586, 169.248928, 174.0701669, 174.6378993, 178.8921776, 183.7141936, 188.5362096, 193.3582256, 198.1802416, 203.0022576, 207.8242736, 212.6462896, 217.4683056, 222.2903216, 227.1123376, 231.9343535, 236.7563695, 237.4562269, 237.4621083, 241.3175674, 241.5774776, 246.3973178, 251.2171579, 256.0369981, 260.8568382, 265.6766783, 270.4965184, 275.3163584, 280.1361985, 284.9560385, 289.7758785, 294.5957185, 299.4155585, 304.2353985, 309.0552385, 313.8750784, 318.6949183, 323.5147582, 328.3345981, 333.154438, 337.9742778, 342.7941177, 347.6139575, 352.4337973, 357.2536371, 362.0734769, 366.8933167, 371.7131564, 376.5329961, 379.5001859, 379.9653547, 381.2994637, 385.7472161, 390.1949684, 394.6427208, 399.0904731, 403.5382255, 407.9859779, 412.4337302, 416.8814826, 421.329235, 425.7769873, 430.2247397, 433.6895388, 434.6725058, 435.8689905, 439.1204164, 443.5683314, 448.0162464, 452.4641615, 456.9120765, 458.1085657]
        y2_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.050217999, -0.200837355, -0.451836987, -0.803167963, -1.254761791, -1.806530432, -2.458366317, -3.210142369, -4.061712028, -5.012909279, -6.063548684, -6.413734814, -7.190090959, -8.321518399, -9.452947078, -10.584377, -11.71580815, -12.84724055, -13.97867419, -15.11010907, -16.24154518, -17.37298254, -18.50442114, -19.63586097, -20.76730205, -21.89874436, -23.03018792, -24.16163271, -25.29307874, -26.42452602, -27.55597453, -28.68742428, -29.81887527, -30.95032751, -32.0817681, -33.21319629, -34.34462455, -35.47605222, -36.60747969, -37.73890716, -38.87033463, -40.0017621, -41.13318926, -42.26461676, -43.39604439, -44.52747213, -45.65890001, -46.790328, -47.92175613, -49.05318437, -50.18461274, -51.31604123, -52.44746985, -53.57889859, -54.71032746, -55.84175644, -56.97318556, -58.10461479, -59.23604415, -60.36747364, -61.49890325, -62.63033298, -63.76176284, -64.30930668, -64.89173391, -65.85012895, -66.01203492, -67.12822406, -68.24441331, -69.36060266, -70.47679213, -71.59298171, -72.7091714, -73.8253612, -74.94155111, -76.05774113, -77.01202512, -77.17393127, -78.29012162, -79.40631209, -80.52250266, -80.91869147, -81.60729243, -82.5505223, -83.34240495, -83.98269916, -84.47120988, -84.60807705, -84.80312882, -84.96202907, -84.94645138, -84.7564005, -84.39193431, -84.22064604, -83.86422386, -83.21218156, -82.43935487, -81.54597922, -80.53232674, -79.39870619, -78.14546288, -76.77297857, -75.28167132, -73.67199541, -71.94444116, -70.09953479, -68.13783828, -67.46831706, -66.08607928, -64.0280633, -61.97004562, -59.91202624, -58.70570393, -57.8417106, -55.6526687, -53.32085888, -50.84699142, -48.23181989, -45.47614089, -42.58079384, -39.54666068, -36.37466563, -33.06577493, -29.62099648, -26.04137961, -22.32801469, -18.48203286, -14.50460563, -10.39694458, -6.160300935, -1.795965215, 2.694733159, 7.310426278, 12.04970815, 16.91113516, 21.89322645, 26.99446444, 32.21329525, 37.54812915, 42.99734112, 48.55927126, 54.23222537, 60.0144754, 65.90426003, 71.89978516, 77.99922451, 84.20072013, 85.48446102, 90.50238298, 96.90229351, 103.3985022, 109.9890304, 116.6718704, 123.4449866, 130.3063158, 137.2537681, 144.2852271, 151.3985511, 158.5915731, 162.5923831, 165.8544652, 170.5162015, 173.1290245, 180.403584, 187.6781435, 194.9527032, 202.2272629, 209.5018227, 216.7763826, 224.0509426, 228.6977002, 231.3255027, 235.33798, 238.6085375, 245.9622594, 253.3973448, 260.9115081, 268.5024395, 276.1678056, 283.90525, 291.7123944, 299.5868387, 307.5261625, 315.5279252, 323.5896671, 331.7089101, 336.5505804, 337.5906902, 339.8808421, 348.1010731, 356.3716227, 364.6899485, 373.0534937, 381.4596871, 389.6503106, 389.9059449, 398.3896706, 406.9082564, 415.4590836, 424.0395239, 432.6469397, 441.2786849, 449.9321063, 456.0451323, 458.60381, 462.8252623, 467.2799295, 469.0593115, 469.6666398, 475.9617225, 484.6628512, 493.3812605, 502.1140359, 507.1031147, 507.8027182, 510.8580272, 519.6107865, 526.7829423, 528.3695111, 537.1302199, 538.1616724, 545.8906766, 554.6511242, 563.4115718, 572.1720193, 580.9324669, 589.6929144, 598.453362, 607.2138095, 615.974257, 624.7347045, 633.495152, 642.2555995, 651.016047, 652.2875202, 652.2982052, 659.303891, 659.7762583, 668.5359565, 677.2956547, 686.0553528, 694.8150509, 703.574749, 712.334447, 721.094145, 729.853843, 738.613541, 747.3732389, 756.1329368, 764.8926347, 773.6523325, 782.4120303, 791.1717281, 799.9314259, 808.6911236, 817.4508213, 826.2105189, 834.9702166, 843.7299142, 852.4896118, 861.2493093, 870.0090068, 878.7687043, 887.5284018, 896.2880992, 905.0477966, 910.4404416, 911.2858662, 913.8361645, 922.7921784, 931.7481923, 940.7042061, 949.66022, 958.6162339, 967.5722478, 976.5282616, 985.4842755, 994.4402894, 1003.396303, 1012.352317, 1019.329052, 1021.308359, 1023.717606, 1030.264691, 1039.221033, 1048.177374, 1057.133715, 1066.090057, 1068.499313]
        z2_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 129.9996751, 139.9974007, 149.9912278, 159.979208, 169.9593942, 179.9298408, 189.8886039, 199.833742, 209.7633164, 219.6753913, 229.5680343, 232.6682863, 239.4445914, 249.3200767, 259.1955616, 269.0710464, 278.9465308, 288.8220149, 298.6974988, 308.5729824, 318.4484658, 328.3239488, 338.1994316, 348.0749141, 357.9503964, 367.8258783, 377.70136, 387.5768414, 397.4523226, 407.3278034, 417.203284, 427.0787643, 436.9542444, 446.8297242, 456.7052065, 466.5806916, 476.4561767, 486.3316619, 496.2071471, 506.0826324, 515.9581176, 525.8336029, 535.7090882, 545.5845734, 555.4600587, 565.3355438, 575.211029, 585.0865141, 594.9619992, 604.8374843, 614.7129694, 624.5884544, 634.4639394, 644.3394244, 654.2149093, 664.0903942, 673.9658791, 683.841364, 693.7168488, 703.5923336, 713.4678184, 723.3433031, 733.2187879, 737.9979335, 743.0918166, 751.5191519, 752.9476399, 762.7957173, 772.6437948, 782.4918722, 792.3399496, 802.188027, 812.0361043, 821.8841816, 831.7322589, 841.5803361, 849.9999254, 851.4284133, 861.2764905, 871.1245676, 880.9726447, 884.4681954, 890.8216829, 900.6736945, 910.5260326, 920.3756958, 930.2196839, 933.7118525, 940.0581585, 949.8991946, 959.7407515, 969.5798313, 979.4134369, 982.9019692, 989.2439398, 999.0871489, 1008.941691, 1018.804565, 1028.672765, 1038.543286, 1048.413122, 1058.279265, 1068.138711, 1077.988456, 1087.8255, 1097.646846, 1107.449504, 1110.66376, 1117.235746, 1127.020785, 1136.805823, 1146.590861, 1152.326431, 1156.373386, 1166.13061, 1175.854691, 1185.542667, 1195.191585, 1204.798507, 1214.360506, 1223.874671, 1233.338102, 1242.747918, 1252.101251, 1261.395253, 1270.627092, 1279.793957, 1288.893055, 1297.921615, 1306.876886, 1315.756141, 1324.556674, 1333.275805, 1341.910879, 1350.459264, 1358.918357, 1367.285582, 1375.558388, 1383.734257, 1391.810698, 1399.785251, 1407.655487, 1415.419008, 1423.07345, 1430.61648, 1438.045801, 1445.359151, 1446.843861, 1452.554301, 1459.62906, 1466.581273, 1473.408821, 1480.109626, 1486.681646, 1493.122879, 1499.431363, 1505.605177, 1511.64244, 1517.541313, 1520.735119, 1523.314217, 1526.999923, 1529.065697, 1534.817177, 1540.568657, 1546.320137, 1552.071616, 1557.823095, 1563.574575, 1569.326054, 1572.999915, 1575.077532, 1578.249914, 1580.814592, 1586.429433, 1591.8986, 1597.220412, 1602.393234, 1607.415475, 1612.285592, 1617.002087, 1621.563511, 1625.968461, 1630.215583, 1634.303573, 1638.231172, 1640.484363, 1640.961344, 1642.004269, 1645.628273, 1649.088549, 1652.384034, 1655.513714, 1658.476628, 1661.189915, 1661.271865, 1663.898566, 1666.355923, 1668.64318, 1670.759635, 1672.704637, 1674.477588, 1676.077944, 1677.102318, 1677.512754, 1678.189914, 1678.904485, 1679.189914, 1679.287335, 1680.248614, 1681.418218, 1682.406057, 1683.2118, 1683.589914, 1683.638753, 1683.839742, 1684.279542, 1684.489914, 1684.51866, 1684.574319, 1684.569389, 1684.523377, 1684.471224, 1684.419069, 1684.366913, 1684.314755, 1684.262595, 1684.210434, 1684.15827, 1684.106105, 1684.053938, 1684.00177, 1683.9496, 1683.897428, 1683.889855, 1683.889792, 1683.792114, 1683.781765, 1683.589858, 1683.397949, 1683.206038, 1683.014126, 1682.822212, 1682.630296, 1682.438378, 1682.246459, 1682.054537, 1681.862614, 1681.67069, 1681.478763, 1681.286835, 1681.094905, 1680.902974, 1680.71104, 1680.519105, 1680.327168, 1680.135229, 1679.943289, 1679.751347, 1679.559403, 1679.367457, 1679.17551, 1678.983561, 1678.79161, 1678.599657, 1678.407703, 1678.289531, 1678.271004, 1678.231056, 1678.145533, 1678.060009, 1677.974485, 1677.888961, 1677.803436, 1677.717912, 1677.632387, 1677.546862, 1677.461337, 1677.375812, 1677.290286, 1677.223662, 1677.209004, 1677.202666, 1677.202666, 1677.202666, 1677.202665, 1677.202665, 1677.202664, 1677.202664]
        y2_northing = [6821995.142 + y2 for y2 in y2_list]
        x2_easting = [13603168.58 - x2 for x2 in x2_list]
        WELL_LAT18 = 61.492317
        WELL_LON18 = 76.937004
        raw_coordinates2 = []
        coordinates2 = []

        ok2 = ~(np.isnan(x2_list) | np.isnan(y2_list) | np.isnan(z2_list))
        dEW2, dNS2, tvd2 = np.array(x2_list)[ok2], np.array(y2_list)[ok2], np.array(z2_list)[ok2]
        tvdss2 = tvd2[-1]
        drilled2 = np.sum(np.sqrt(np.diff(dEW2)**2 + np.diff(dNS2)**2 + np.diff(tvd2)**2))

        tooltip2_head = folium.Tooltip(html2_wellhead_small, sticky=False, direction='top')
        folium.Marker(location=[61.492317, 76.937004],
            tooltip=tooltip2_head,
            popup=html2_wellhead_full.format(drilled2=f'{drilled2:.0f}m.'),
            icon=folium.CustomIcon(image, icon_size=(44, 46), icon_anchor=(22, 46))
        ).add_to(m)

        for x, y in zip(x2_easting, y2_northing):
            if np.isnan(x) or np.isnan(y):
                continue
            lon, lat = transformer.transform(x, y)
            raw_coordinates2.append((lat, lon))

        delta_lat = WELL_LAT18 - raw_coordinates2[0][0]
        delta_lon = WELL_LON18 - raw_coordinates2[0][1]
        for lat, lon in raw_coordinates2:
            coordinates2.append((lat + delta_lat, lon + delta_lon))

        AntPath(
            locations=coordinates2,
            delay=1200,
            dash_array=[10, 50],
            color='#FFFF00',
            pulse_color='#000000',
            weight=6,
            opacity=0.5,
            tooltip=html2_trajectory
        ).add_to(m)

        last_lat2, last_lon2 = coordinates2[-1]
        tooltip2_bottom = folium.Tooltip(html2_wellbottom_small, sticky=False, direction='top')
        folium.CircleMarker(
            location=[last_lat2, last_lon2],
            radius=8,
            color="#FFFF00",
            opacity=1.0,
            fill=True,
            fill_color="#000000",
            fill_opacity=0.8,
            tooltip=tooltip2_bottom,
            popup=html2_wellbottom_full.format(tvdss2=f'{tvdss2:.0f}m.'),
        ).add_to(m)

        html3_wellhead_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Well: SIBWELL19(head)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Status</span>
                    Digging
                </div>
                <div class="popup-row">
                    <span class="label">Start date</span>
                    17.01.2023
                </div>
                <div class="popup-row">
                    <span class="label">Drilling meterage</span>
                    {drilled3}
                </div>
            </div>
        </div>
        '''

        html3_wellhead_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL19(head)
        </div>
        '''

        html3_wellbottom_full = '''
        <div class="popup-box">
            <div class="popup-header">
                Well: SIBWELL19(bottom)
            </div>
            <div class="popup-content">
                <div class="popup-row">
                    <span class="label">Depth</span>
                    {tvdss3}
                </div>
            </div>
        </div>
        '''

        html3_wellbottom_small = '''
        <div class="custom-tooltip">
            Well: SIBWELL19(bottom)
        </div>
        '''

        html3_trajectory = '''
        <div class="custom-trajectory">
            Wellbore trajectory to the bottom of SIBWELL19
        </div>
        '''

        x3_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.048512693, -0.194017306, -0.436493476, -0.775893931, -1.212152505, -1.745184148, -2.374884945, -3.101132135, -3.923784133, -4.842680563, -5.857642283, -6.195936769, -6.945929359, -8.038935708, -9.131943255, -10.224952, -11.31796194, -12.41097308, -13.50398542, -14.59699895, -15.69001368, -16.78302961, -17.87604674, -18.96906506, -20.06208458, -21.1551053, -22.24812722, -23.34115034, -24.43417465, -25.52720016, -26.62022686, -27.71325477, -28.80628387, -29.89931417, -30.99233323, -32.0853403, -33.17834744, -34.27135402, -35.36436039, -36.45736677, -37.55037315, -38.64337953, -39.73638561, -40.82939202, -41.92239855, -43.01540519, -44.10841196, -45.20141885, -46.29442586, -47.38743298, -48.48044023, -49.5734476, -50.66645509, -51.75946269, -52.85247042, -53.94547826, -55.03848623, -56.13149432, -57.22450252, -58.31751085, -59.41051929, -60.50352785, -61.59653654, -62.12548685, -62.71260746, -63.78669764, -63.97964967, -65.30987208, -66.64009462, -67.9703173, -69.30054011, -70.63076305, -71.96098612, -73.29120932, -74.62143266, -75.95165612, -77.08892751, -77.28187974, -78.6121036, -79.9423276, -81.27255172, -81.74471116, -82.62098482, -84.05124512, -85.56841979, -87.17204666, -88.86163728, -89.48192844, -90.61998999, -92.38810203, -94.16038217, -95.93629056, -97.71528623, -98.34737649, -99.47040867, -101.1085587, -102.6212381, -104.007986, -105.26838, -106.4020362, -107.4086093, -108.2877926, -109.0393184, -109.6629578, -110.1585207, -110.5258561, -110.7648524, -110.8153267, -110.9044054, -111.0370348, -111.1696644, -111.302294, -111.3800358, -111.4268109, -111.4728567, -111.4241449, -111.2806903, -111.0425367, -110.7097565, -110.2824513, -109.760751, -109.1448147, -108.43483, -107.6310131, -106.7336088, -105.7428906, -104.6591602, -103.4827477, -102.2140115, -100.8533381, -99.40114186, -97.85786521, -96.22397823, -94.49997862, -92.68639153, -90.78376939, -88.79269176, -86.71376514, -84.54762279, -82.29492454, -79.95635659, -77.53263128, -75.0244869, -72.43268746, -69.75802245, -67.0013066, -64.16337962, -63.57165203, -61.24510598, -58.24737461, -55.17109866, -52.01721518, -48.78668487, -45.48049179, -42.09964304, -38.64516846, -35.11812031, -31.51957296, -27.85062257, -25.79719509, -24.11927293, -21.72140848, -20.3774467, -16.6356204, -12.89379406, -9.151967667, -5.410141231, -1.668314748, 2.073511781, 5.815338355, 8.205498194, 9.557164992, 11.62106913, 13.30455592, 17.09846898, 20.94621563, 24.84661309, 28.79846237, 32.80054871, 36.85164187, 40.95049657, 45.09585283, 49.28643639, 53.52095908, 57.79811922, 62.11660202, 64.69687503, 65.25158387, 66.47337636, 70.86562365, 75.29528908, 79.76101098, 84.26141662, 88.79512257, 93.22240237, 93.36073521, 97.95685107, 102.5820573, 107.2349322, 111.9140455, 116.6179587, 121.345226, 126.0943942, 129.4553574, 130.8631657, 133.1858481, 135.6368474, 136.6158799, 136.9500376, 140.4136507, 145.2010926, 149.9980425, 154.8028968, 157.5479344, 157.9328627, 159.6139222, 164.4297717, 168.3759586, 169.248928, 174.0701669, 174.6378993, 178.8921776, 183.7141936, 188.5362096, 193.3582256, 198.1802416, 203.0022576, 207.8242736, 212.6462896, 217.4683056, 222.2903216, 227.1123376, 231.9343535, 236.7563695, 237.4562269, 237.4621083, 241.3175674, 241.5774776, 246.3973178, 251.2171579, 256.0369981, 260.8568382, 265.6766783, 270.4965184, 275.3163584, 280.1361985, 284.9560385, 289.7758785, 294.5957185, 299.4155585, 304.2353985, 309.0552385, 313.8750784, 318.6949183, 323.5147582, 328.3345981, 333.154438, 337.9742778, 342.7941177, 347.6139575, 352.4337973, 357.2536371, 362.0734769, 366.8933167, 371.7131564, 376.5329961, 379.5001859, 379.9653547, 381.2994637, 385.7472161, 390.1949684, 394.6427208, 399.0904731, 403.5382255, 407.9859779, 412.4337302, 416.8814826, 421.329235, 425.7769873, 430.2247397, 433.6895388, 434.6725058, 435.8689905, 439.1204164, 443.5683314, 448.0162464, 452.4641615, 456.9120765, 458.1085657]
        y3_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.050217999, -0.200837355, -0.451836987, -0.803167963, -1.254761791, -1.806530432, -2.458366317, -3.210142369, -4.061712028, -5.012909279, -6.063548684, -6.413734814, -7.190090959, -8.321518399, -9.452947078, -10.584377, -11.71580815, -12.84724055, -13.97867419, -15.11010907, -16.24154518, -17.37298254, -18.50442114, -19.63586097, -20.76730205, -21.89874436, -23.03018792, -24.16163271, -25.29307874, -26.42452602, -27.55597453, -28.68742428, -29.81887527, -30.95032751, -32.0817681, -33.21319629, -34.34462455, -35.47605222, -36.60747969, -37.73890716, -38.87033463, -40.0017621, -41.13318926, -42.26461676, -43.39604439, -44.52747213, -45.65890001, -46.790328, -47.92175613, -49.05318437, -50.18461274, -51.31604123, -52.44746985, -53.57889859, -54.71032746, -55.84175644, -56.97318556, -58.10461479, -59.23604415, -60.36747364, -61.49890325, -62.63033298, -63.76176284, -64.30930668, -64.89173391, -65.85012895, -66.01203492, -67.12822406, -68.24441331, -69.36060266, -70.47679213, -71.59298171, -72.7091714, -73.8253612, -74.94155111, -76.05774113, -77.01202512, -77.17393127, -78.29012162, -79.40631209, -80.52250266, -80.91869147, -81.60729243, -82.5505223, -83.34240495, -83.98269916, -84.47120988, -84.60807705, -84.80312882, -84.96202907, -84.94645138, -84.7564005, -84.39193431, -84.22064604, -83.86422386, -83.21218156, -82.43935487, -81.54597922, -80.53232674, -79.39870619, -78.14546288, -76.77297857, -75.28167132, -73.67199541, -71.94444116, -70.09953479, -68.13783828, -67.46831706, -66.08607928, -64.0280633, -61.97004562, -59.91202624, -58.70570393, -57.8417106, -55.6526687, -53.32085888, -50.84699142, -48.23181989, -45.47614089, -42.58079384, -39.54666068, -36.37466563, -33.06577493, -29.62099648, -26.04137961, -22.32801469, -18.48203286, -14.50460563, -10.39694458, -6.160300935, -1.795965215, 2.694733159, 7.310426278, 12.04970815, 16.91113516, 21.89322645, 26.99446444, 32.21329525, 37.54812915, 42.99734112, 48.55927126, 54.23222537, 60.0144754, 65.90426003, 71.89978516, 77.99922451, 84.20072013, 85.48446102, 90.50238298, 96.90229351, 103.3985022, 109.9890304, 116.6718704, 123.4449866, 130.3063158, 137.2537681, 144.2852271, 151.3985511, 158.5915731, 162.5923831, 165.8544652, 170.5162015, 173.1290245, 180.403584, 187.6781435, 194.9527032, 202.2272629, 209.5018227, 216.7763826, 224.0509426, 228.6977002, 231.3255027, 235.33798, 238.6085375, 245.9622594, 253.3973448, 260.9115081, 268.5024395, 276.1678056, 283.90525, 291.7123944, 299.5868387, 307.5261625, 315.5279252, 323.5896671, 331.7089101, 336.5505804, 337.5906902, 339.8808421, 348.1010731, 356.3716227, 364.6899485, 373.0534937, 381.4596871, 389.6503106, 389.9059449, 398.3896706, 406.9082564, 415.4590836, 424.0395239, 432.6469397, 441.2786849, 449.9321063, 456.0451323, 458.60381, 462.8252623, 467.2799295, 469.0593115, 469.6666398, 475.9617225, 484.6628512, 493.3812605, 502.1140359, 507.1031147, 507.8027182, 510.8580272, 519.6107865, 526.7829423, 528.3695111, 537.1302199, 538.1616724, 545.8906766, 554.6511242, 563.4115718, 572.1720193, 580.9324669, 589.6929144, 598.453362, 607.2138095, 615.974257, 624.7347045, 633.495152, 642.2555995, 651.016047, 652.2875202, 652.2982052, 659.303891, 659.7762583, 668.5359565, 677.2956547, 686.0553528, 694.8150509, 703.574749, 712.334447, 721.094145, 729.853843, 738.613541, 747.3732389, 756.1329368, 764.8926347, 773.6523325, 782.4120303, 791.1717281, 799.9314259, 808.6911236, 817.4508213, 826.2105189, 834.9702166, 843.7299142, 852.4896118, 861.2493093, 870.0090068, 878.7687043, 887.5284018, 896.2880992, 905.0477966, 910.4404416, 911.2858662, 913.8361645, 922.7921784, 931.7481923, 940.7042061, 949.66022, 958.6162339, 967.5722478, 976.5282616, 985.4842755, 994.4402894, 1003.396303, 1012.352317, 1019.329052, 1021.308359, 1023.717606, 1030.264691, 1039.221033, 1048.177374, 1057.133715, 1066.090057, 1068.499313]
        z3_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 129.9996751, 139.9974007, 149.9912278, 159.979208, 169.9593942, 179.9298408, 189.8886039, 199.833742, 209.7633164, 219.6753913, 229.5680343, 232.6682863, 239.4445914, 249.3200767, 259.1955616, 269.0710464, 278.9465308, 288.8220149, 298.6974988, 308.5729824, 318.4484658, 328.3239488, 338.1994316, 348.0749141, 357.9503964, 367.8258783, 377.70136, 387.5768414, 397.4523226, 407.3278034, 417.203284, 427.0787643, 436.9542444, 446.8297242, 456.7052065, 466.5806916, 476.4561767, 486.3316619, 496.2071471, 506.0826324, 515.9581176, 525.8336029, 535.7090882, 545.5845734, 555.4600587, 565.3355438, 575.211029, 585.0865141, 594.9619992, 604.8374843, 614.7129694, 624.5884544, 634.4639394, 644.3394244, 654.2149093, 664.0903942, 673.9658791, 683.841364, 693.7168488, 703.5923336, 713.4678184, 723.3433031, 733.2187879, 737.9979335, 743.0918166, 751.5191519, 752.9476399, 762.7957173, 772.6437948, 782.4918722, 792.3399496, 802.188027, 812.0361043, 821.8841816, 831.7322589, 841.5803361, 849.9999254, 851.4284133, 861.2764905, 871.1245676, 880.9726447, 884.4681954, 890.8216829, 900.6736945, 910.5260326, 920.3756958, 930.2196839, 933.7118525, 940.0581585, 949.8991946, 959.7407515, 969.5798313, 979.4134369, 982.9019692, 989.2439398, 999.0871489, 1008.941691, 1018.804565, 1028.672765, 1038.543286, 1048.413122, 1058.279265, 1068.138711, 1077.988456, 1087.8255, 1097.646846, 1107.449504, 1110.66376, 1117.235746, 1127.020785, 1136.805823, 1146.590861, 1152.326431, 1156.373386, 1166.13061, 1175.854691, 1185.542667, 1195.191585, 1204.798507, 1214.360506, 1223.874671, 1233.338102, 1242.747918, 1252.101251, 1261.395253, 1270.627092, 1279.793957, 1288.893055, 1297.921615, 1306.876886, 1315.756141, 1324.556674, 1333.275805, 1341.910879, 1350.459264, 1358.918357, 1367.285582, 1375.558388, 1383.734257, 1391.810698, 1399.785251, 1407.655487, 1415.419008, 1423.07345, 1430.61648, 1438.045801, 1445.359151, 1446.843861, 1452.554301, 1459.62906, 1466.581273, 1473.408821, 1480.109626, 1486.681646, 1493.122879, 1499.431363, 1505.605177, 1511.64244, 1517.541313, 1520.735119, 1523.314217, 1526.999923, 1529.065697, 1534.817177, 1540.568657, 1546.320137, 1552.071616, 1557.823095, 1563.574575, 1569.326054, 1572.999915, 1575.077532, 1578.249914, 1580.814592, 1586.429433, 1591.8986, 1597.220412, 1602.393234, 1607.415475, 1612.285592, 1617.002087, 1621.563511, 1625.968461, 1630.215583, 1634.303573, 1638.231172, 1640.484363, 1640.961344, 1642.004269, 1645.628273, 1649.088549, 1652.384034, 1655.513714, 1658.476628, 1661.189915, 1661.271865, 1663.898566, 1666.355923, 1668.64318, 1670.759635, 1672.704637, 1674.477588, 1676.077944, 1677.102318, 1677.512754, 1678.189914, 1678.904485, 1679.189914, 1679.287335, 1680.248614, 1681.418218, 1682.406057, 1683.2118, 1683.589914, 1683.638753, 1683.839742, 1684.279542, 1684.489914, 1684.51866, 1684.574319, 1684.569389, 1684.523377, 1684.471224, 1684.419069, 1684.366913, 1684.314755, 1684.262595, 1684.210434, 1684.15827, 1684.106105, 1684.053938, 1684.00177, 1683.9496, 1683.897428, 1683.889855, 1683.889792, 1683.792114, 1683.781765, 1683.589858, 1683.397949, 1683.206038, 1683.014126, 1682.822212, 1682.630296, 1682.438378, 1682.246459, 1682.054537, 1681.862614, 1681.67069, 1681.478763, 1681.286835, 1681.094905, 1680.902974, 1680.71104, 1680.519105, 1680.327168, 1680.135229, 1679.943289, 1679.751347, 1679.559403, 1679.367457, 1679.17551, 1678.983561, 1678.79161, 1678.599657, 1678.407703, 1678.289531, 1678.271004, 1678.231056, 1678.145533, 1678.060009, 1677.974485, 1677.888961, 1677.803436, 1677.717912, 1677.632387, 1677.546862, 1677.461337, 1677.375812, 1677.290286, 1677.223662, 1677.209004, 1677.202666, 1677.202666, 1677.202666, 1677.202665, 1677.202665, 1677.202664, 1677.202664]
        y3_northing = [6820277.435 + y3 for y3 in y3_list]
        x3_easting = [13546423.742 - x3 for x3 in x3_list]
        WELL_LAT19 = 61.488036
        WELL_LON19 = 75.871453
        raw_coordinates3 = []
        coordinates3 = []

        ok3 = ~(np.isnan(x3_list) | np.isnan(y3_list) | np.isnan(z3_list))
        dEW3, dNS3, tvd3 = np.array(x3_list)[ok3], np.array(y3_list)[ok3], np.array(z3_list)[ok3]
        tvdss3 = tvd3[-1]
        drilled3 = np.sum(np.sqrt(np.diff(dEW3)**2 + np.diff(dNS3)**2 + np.diff(tvd3)**2))

        tooltip3_head = folium.Tooltip(html3_wellhead_small, sticky=False, direction='top')
        folium.Marker(location=[61.488036, 75.871453],
            tooltip=tooltip3_head,
            popup=html3_wellhead_full.format(drilled3=f'{drilled3:.0f}m.'),
            icon=folium.CustomIcon(image, icon_size=(44, 46), icon_anchor=(22, 46))
        ).add_to(m)

        for x, y in zip(x3_easting, y3_northing):
            if np.isnan(x) or np.isnan(y):
                continue
            lon, lat = transformer.transform(x, y)
            raw_coordinates3.append((lat, lon))

        delta_lat = WELL_LAT19 - raw_coordinates3[0][0]
        delta_lon = WELL_LON19 - raw_coordinates3[0][1]
        for lat, lon in raw_coordinates3:
            coordinates3.append((lat + delta_lat, lon + delta_lon))

        AntPath(
            locations=coordinates3,
            delay=1200,
            dash_array=[10, 50],
            color='#FFFF00',
            pulse_color='#000000',
            weight=6,
            opacity=0.5,
            tooltip=html3_trajectory
        ).add_to(m)

        last_lat3, last_lon3 = coordinates3[-1]
        tooltip3_bottom = folium.Tooltip(html3_wellbottom_small, sticky=False, direction='top')
        folium.CircleMarker(
            location=[last_lat3, last_lon3],
            radius=8,
            color="#FFFF00",
            opacity=1.0,
            fill=True,
            fill_color="#000000",
            fill_opacity=0.8,
            tooltip=tooltip3_bottom,
            popup=html3_wellbottom_full.format(tvdss3=f'{tvdss3:.0f}m.'),
        ).add_to(m)


        map_html = m._repr_html_()
        self.browser.setHtml(map_html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())