# import af2_features
import pickle

bm40 = pickle.load(open("./experiment/benchmark40_name2id.pkl", "rb"))
data = pickle.load(open("./experiment/files/tmp_1.0_p_0.0_k_5_prefix_6_res.pkl", "rb"))
case2ft = {}
for case in bm40.keys():
    q_seq = data[case]["query"]
    msa = data[case]["context"]
    msa = [m[0] for m in msa]
    case2ft[case] = {
        1: af2_features.construct_MSAFt_from_msa(q_seq, msa[:1]),
        3: af2_features.construct_MSAFt_from_msa(q_seq, msa[:3]),
        6: af2_features.construct_MSAFt_from_msa(q_seq, msa[:6])
    }
print(len(case2ft))
breakpoint()
pickle.dump(case2ft, open("./bm40case2ft.pkl", "wb"))

case2msa = {}
for case in bm40.keys():
    msa = data[case]["context"]
    case2msa[case] = {
        1: [m[0] for m in msa[:1]],
        3: [m[0] for m in msa[:3]],
        6: [m[0] for m in msa[:6]],
    }
print(len(case2msa))
pickle.dump(case2msa, open("./MSA-Augmentor-master/dataset/bm40case2msa.pkl", "wb"))

case2query = {}
for case in bm40.keys():
    case2query[case] = data[case]["query"]
print(len(case2query))
pickle.dump(case2query, open("./MSA-Augmentor-master/dataset/bm40case2query.pkl", "wb"))