
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
#     fieldindicatos.forEach(feature_ => {
#       feature_.year = parseInt(feature_.year)
#       if (feature_.year === 2020) {
#         // let existing_ft_data = response.data.find(ft_data => {
#         //   if (feature_.field_id === ft_data.field_id && ft_data.year === 2020) {
#         //     return ft_data
#         //   }
#         //   return null
#         // })
#         let ft_data_2019 = fieldindicatos.find(ft_ => {
#           if (ft_.year === 2019 && ft_.field_id === feature_.field_id) {
#             return ft_
#           }
#           return null
#         })
#         // let missing_months = [/*"september",*/ "october", "november"]
#         // missing_months.forEach(month_ => {
#         //   feature_.field_rainfall[month_] = ""
#         //   feature_.field_ndvi[month_] = ""
#         //   feature_.field_ndwi[month_] = ""
#         //   feature_.field_temperature[month_] = ""
#         // })
#         // console.log(feature_, "mmmmmm", ft_data_2019)
#         feature_.field_rainfall.december = ft_data_2019.field_rainfall.december
#         feature_.field_ndvi.december = ft_data_2019.field_ndvi.december
#         feature_.field_ndwi.december = ft_data_2019.field_ndwi.december
#         feature_.field_temperature.december = ft_data_2019.field_temperature.december
#         // this.props.dispatch(getcreateputGraphData(
#         //  feature_, 'POST', ""
#         // ))
#         // if (!existing_ft_data) {
#         //   count += 1
#         // }
#       }
#     })
#     // console.log(fieldindicatos)
#     // TESTING THAT WE HAVE THE RIGHT DATA
#     // this.props.dispatch(getcreateputGraphData(
#     //  fieldindicatos[0], 'POST', ""
#     // ))
#   })
# // this.props.postPolygonLayer(farmAfrica.features[0])


"""As of 4th DEECEMBER"""
#     // console.log(fields_)
#     let count = 0
#     fields_.features.forEach(feature => {
#       feature.properties.field_attributes = {}
#       feature.properties.user_id = ""
#       feature.properties.field_attributes.CropType = "Coffee"
#       let keys_ = Object.keys(feature.properties)
#       keys_.forEach(key => {
#         if (!["user_id", "field_attributes", "field_id"].includes(key)) {
#           if (feature.properties[key] === null) {
#             feature.properties[key] = ""
#           }
#           // croptype is below
#           if (key === "Select Value chain") {
#             // console.log("count")
#             feature.properties.field_attributes.CropType = feature.properties[key]
#             delete feature.properties[key]
#           } else {
#             feature.properties.field_attributes[key] =
#              feature.properties[key]
#             delete feature.properties[key]
#           }
#         }
#       })
#       let already_there = leafletGeoJSON.features.find(ft_ => {
#         if (ft_.properties.field_id === feature.properties.field_id) {
#           return ft_
#         }
#         return null
#       })
#       if (!already_there){
#         count += 1
#         // this.props.postPolygonLayer(feature)
#       }
#     })