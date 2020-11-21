
import pandas as pd

df = pd.read_csv('')
df_2019 = df[~df.Year.isin([2020])]
# check on 2020_exists
df_me.iloc[1]
df_2019.to_csv('')

"""js scripts"""
"""MORINGA CONNECT"""
# axiosInstance({
#   url: `/layers/fieldindicators/`,
#   method: "GET",
#   data: ""
# })
#   .then(async response => {
#     let feature_ids = response.data.map(feature_ => feature_.field_id)
#     console.log(feature_ids.length)
#     farmAfrica.forEach(
#       feature_ => {
#       //   feature_.properties.field_attributes = {}
#       //   feature_.properties.user_id = ""
#       //   feature_.properties.field_attributes["Farmer ID"] =
#       //    feature_.properties["Farmer ID"]
#       //   delete feature_.properties["Farmer ID"]
#       //   feature_.properties["Farmer name"] =
#       //    feature_.properties.field_attributes["Farmer name"]
#       //   delete feature_.properties["Farmer name"]
#       //   feature_.properties.field_attributes.CropType = "moringa"
#         if (!feature_ids.includes(feature_.field_id)) {
#           // this.props.postPolygonLayer(feature_)
#           console.log(JSON.parse(JSON.stringify("hhhh")))
#             this.props.dispatch(getcreateputGraphData(
#               feature_, 'POST', ""
#             ))
#         }

#         // if (feature_.year === 2019) {
#         //   this.props.dispatch(getcreateputGraphData(
#         //     feature_, 'POST', ""
#         //   ))
#         // }
#       }
#     )
#   })
# // this.props.postPolygonLayer(farmAfrica.features[0])
